import os as sys
path='./test_cases/yaSater'
num_of_test_cases=10
files=['input.json','models.json','specialized_quest_types.json','pure_query.json','ready_query.json','on_going_query.json','gathered_query.json']
def is_empty():
    directories=[]
    for file in sys.scandir(path):
        directories.append(file)
    return len(directories)==0

def create_base():
    if is_empty():
        for i in range(num_of_test_cases):
            file_name=sys.path.join(path,f'{i}')
            sys.makedirs(file_name,exist_ok=False)

            for file in files:
                with open(sys.path.join(file_name,file), 'w') as f:
                    pass



create_base()
