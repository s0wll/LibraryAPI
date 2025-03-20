async def test_users_api_flow(authentificated_admin_ac):
    # /get_all_users
    response_get_all_users = await authentificated_admin_ac.get("/users")
    assert response_get_all_users.status_code == 200

    # /get_current_user_role
    response_get_current_user_role = await authentificated_admin_ac.get("/users/{user_id}")
    assert response_get_current_user_role.status_code == 200
    res = response_get_current_user_role.json()
    assert res == "Вы являетесь администратором"

    # /assign_current_user_role
    response_assign_user_role = await authentificated_admin_ac.put(
        "/users/3/role", json={"is_admin": True}
    )
    assert response_assign_user_role.status_code == 200
    assert response_assign_user_role.json()["status"] == "OK"

    # /update_user
    response_update_user = await authentificated_admin_ac.patch(
        "/users/{user_id}", json={"email": "admin_updated@gmail.com", "username": "admin_updated"}
    )
    assert response_update_user.status_code == 200
    assert response_update_user.json()["status"] == "OK"
