

def get_mail_text(link_type: str):
    isReset = link_type == "reset";

    return {
    'btn_text': 'Reset Password' if isReset else 'Verify Email',
    'title': 'Reset Your Password' if isReset else 'Verify Your Email',
    'content': f'<h2>Please click on the given link to {"reset your password" if isReset else "verify your email"}!</h2>',
    'link_type': link_type,
    'action': 'resetting password' if isReset else 'email verification'
}
