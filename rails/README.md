# Ruby on Rails 5 API Authentation Example App

This is an example Rails API with JWT-based authentication and user registration.

## Dependencies

* Ruby 2
* Ruby on Rails 5
* PostgreSQL

## Install and Start Server

```
bundle install
bin/rails db:setup
bin/rails s
```

## Example API Requests

Examples below with [httpie](https://httpie.org):

```
export BASE_URL=http://localhost:3000

# Successful register (=> 201)
echo '{"user": {"email": "admin@example.com", "password": "123"}}' | http POST $BASE_URL/register

# Failed register (=> 422)
echo '{"user": {"email": "admin@example.com", "password": "123"}}' | http POST $BASE_URL/register

# Successful login (=> 200, returns token)
echo '{"email": "admin@example.com", "password": "123"}' | http POST $BASE_URL/login
export TOKEN=<token-in-response-above>

# Failed login attempt (=> 401)
echo '{"email": "admin@example.com", "password": "122"}' | http POST $BASE_URL/login

# Successful get user info (=> 200, returns recent_logins)
http $BASE_URL/me Authorization:"Bearer $TOKEN"

# Failed get user info (=> 401)
http $BASE_URL/me
```

## TODO

* Don't expose password_digest
* Tests
* Heroku deployment

## How this App was Created

```
rails new api-auth --database=postgresql --api
cd api-auth

bin/rails g model User name email password_digest recent_logins:jsonb
# Added to migration:
# null: false to email and password_digest columns
# add_index :users, [:email], :unique => true
bin/rails db:create
bin/rails db:migrate

# Add gem 'jwt' and gem 'bcrypt' to Gemfile
bundle install
# Add has_secure_password to user.rb (handles password encryption, limits password length to 72 characters)

bin/rails c
User.create!(email: 'admin@example.com' , password: '123')
User.find_by(email: 'admin@example.com')
exit

bin/rails db
select * from users;
\q

bin/rails g controller users register login me

# Modified routes in config/routes.rb
# post 'register', to: 'users/register'
# post 'login', to: 'users/login'
# get 'me', to: 'users/me'

# Added application code in these files:
# app/models/user.rb
# app/models/auth_token.rb
# config/initializers/auth_token.rb
# app/controllers/application_controller.rb
# app/controllers/users_controller.rb
```

## Resources

* [Token-based authentication with Ruby on Rails 5 API](https://www.pluralsight.com/guides/ruby-ruby-on-rails/token-based-authentication-with-ruby-on-rails-5-api)
