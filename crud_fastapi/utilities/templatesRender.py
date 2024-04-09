from jinja2 import Environment, FileSystemLoader

loader = FileSystemLoader('crud_fastapi/templates/build')
env = Environment(loader=loader)

def Render(file:str, **kwargs:int | str | dict[str] | None) -> str:
    '''
    ### Receive a file and return it rendered by jinja2
    @params file -> file template to be rendered
    @params kwargs -> single string or dict of strings to replace in file template
    @return a string with file template content replaced by
    '''
    return env.get_template(file).render(**kwargs)