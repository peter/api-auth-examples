Rails.application.routes.draw do
  post 'register', to: 'users#register'
  post 'login', to: 'users#login'
  get 'me', to: 'users#me'
end
