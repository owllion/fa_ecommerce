from ...schemas import email_schema
from .get_html_template import get_html_template 

def set_template(params: email_schema.CreateEmailContentSchema) -> str:
  return get_html_template(params)