def super_admin_invite(name: str, invite_url: str, expiry_hours: int):
    return f"""
    <h2>Super Admin Access Granted</h2>

    <p>Hello {name},</p>

    <p>You now have <b>Super Admin</b> privileges.</p>

    <p><a href="{invite_url}">Activate Access</a></p>

    <p>This link expires in {expiry_hours} hours.</p>
    """


def admin_invite(name: str, invite_url: str, expiry_hours: int):
    return f"""
    <h2>Welcome to PMO Platform</h2>

    <p>Hello {name},</p>

    <p>You have been invited as an <b>Admin</b>.</p>

    <p><a href="{invite_url}">Activate Account</a></p>

    <p>This link expires in {expiry_hours} hours.</p>
    """


def manager_invite(name: str, invite_url: str, expiry_hours: int):
    return f"""
    <h2>PMO Invitation</h2>

    <p>Hello {name},</p>

    <p>You have been invited as a <b>Project Manager</b>.</p>

    <p><a href="{invite_url}">Complete Setup</a></p>
    <p>This link expires in {expiry_hours} hours.</p>
    """


def employee_invite(name: str, invite_url: str, expiry_hours: int):
    return f"""
    <h2>You are invited 🎉</h2>

    <p>Hello {name},</p>

    <p>You have been added as an <b>Employee</b>.</p>

    <p><a href="{invite_url}">Set Your Password</a></p>
    <p>This link expires in {expiry_hours} hours.</p>
    """
def get_invite_email(role_id: int, name: str, invite_url: str, expiry_hours: int):
    if role_id == 1:
        return super_admin_invite(name, invite_url, expiry_hours)
    elif role_id == 2:
        return admin_invite(name, invite_url, expiry_hours)
    elif role_id == 3:
        return manager_invite(name, invite_url, expiry_hours)
    elif role_id == 4:
        return employee_invite(name, invite_url, expiry_hours)
    else:
        return employee_invite(name, invite_url, expiry_hours)
