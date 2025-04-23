from backend import tracer

# ref = config.get(name='specialized_quest_types')

# noinspection PyDictCreation
def test_case_1():

    inputs1 = {}

    # this is incorrect, and has to be reviewed
    inputs1['content']={}
    inputs=inputs1['content']
    inputs['model_id']="chexpert001"
    inputs['types'] = ['image']
    inputs['image'] = ['radiograph']
    inputs['radiograph'] = ['chest']
    inputs['chest'] = [0]
    inputs[0]=['/home/omarshagar/Pictures/index.jpeg','/home/omarshagar/Pictures/index.jpeg']
    
    tracer.pipeline.query_to_pure(command='predict', inputs=inputs1)
    
if __name__ == '__main__':

    test_case_1()

