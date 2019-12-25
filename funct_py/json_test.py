import json
j = json.loads('{"tabs":[{"index":0,"current_file":{"path":"/home/sakuk/Documents/Hero/funct_py","is_dir":true,"content":["main.py","render.py","__pycache__","models.py","eventHandler.py"],"content_size":5},"selected_file":{"path":"/home/sakuk/Documents/Hero/funct_py/main.py","is_dir":false,"content":["import curses"],"content_size":2452},"parent_file":{"path":"/home/sakuk/Documents/Hero","is_dir":true,"content":[".git",".gitignore","todo.txt","__pycache__","README.md","hero","funct_py"],"content_size":7}}],"selected_tab":0,"clipbord":null,"mode":0,"exit":false}')

print(json.dumps(j, indent=4).split("\n"))
