require 'test_helper'

class UsersControllerTest < ActionDispatch::IntegrationTest
  test "should get register" do
    get users_register_url
    assert_response :success
  end

  test "should get login" do
    get users_login_url
    assert_response :success
  end

  test "should get me" do
    get users_me_url
    assert_response :success
  end

end
