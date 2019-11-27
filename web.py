from pywebcopy import save_website

kwargs = {'project_name': 'website downloaded'}

save_website(
    url='https://www.tutorialspoint.com',
    project_folder='',
    **kwargs
)