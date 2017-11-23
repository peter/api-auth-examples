class User < ApplicationRecord
  RECENT_LOGINS_LIMIT = 5
  has_secure_password
  validates :email, uniqueness: true

  def auth_token
    AuthToken.encode({user_id: id})
  end

  def save_recent_login!(success)
    login = {time: Time.zone.now}
    attribute = success ? :recent_successful_logins : :recent_failed_logins
    self.send("#{attribute}=", ([login] + (self.send(attribute) || [])).first(RECENT_LOGINS_LIMIT))
    save!
  end
end
