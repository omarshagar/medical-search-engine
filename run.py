import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

from ui.src.config import Config

from ui.src.handlers.screen import Screen
from ui.src.handlers.home import HomePage
from ui.src.handlers.profile import Profile

from ui.src.models.specialized_quest import SpecializedQuestModel
from ui.src.models.query import QueryModel
from ui.src.models.report import ReportModel

from ui.src.utils import testing

def run_qml():
            
    # ======================================================================================================================================

    # specialized quest: random graph (these lines are being used for testing)
    # Config.specialized_quest_types = testing.random_graph(max_nodes_per_level=25, max_depth=6, childs_key='childs')
    # SpecializedQuestModel.reference = Config.get_clustered_reference().copy()
    # SpecializedQuestModel.items_dictionary = Config.get_specialization_items_dictionary(default=None).copy()
    # SpecializedQuestModel.base_level = 0
    
    # print('Ready!')
    
    # specialized quest: model initialization    
    sq_model = SpecializedQuestModel(roles=['name', 'iconUrl', 'selected', 'status'])

    # set start level | if not on the testing mode, the top most base_level is 1.
    sq_model.set_specialization_level_at(level=sq_model.base_level)

    # sq_model.next()
    
    # print(sq_model.items)

    # ======================================================================================================================================

    query_model = QueryModel(roles=['title', 'profile', 'iconUrl', 'selected', 'status', 'data'])

    # query_model.reset(profiles_id=['chexpert001'])

    # query_model.getProfile(index=0)
    
    # ======================================================================================================================================
    
    
    report_model = ReportModel(roles=['report_id', 'profile', 'placeholderType', 
                                    'placeholderUrl', 'header', 'status', 'outputs_model'])
    
    # for i in range(50):
        
    #     report_model.appendReport(f'report{i}', 'chexpert001')
    
    # report_model.setOutputs(0, outputs=[
    #     {'type': 'image', 'certainty': '100%', 'tags': ['no finding'], 'data': [Config.Icons['missing'], Config.Icons['corrupted_image']], 'is_stream': False}
    # ])
    
    # ======================================================================================================================================

    sq_model.set_query_model(query_model=query_model)
    query_model.set_report_model(report_model=report_model)
    report_model.set_query_model(query_model=query_model)

    # ======================================================================================================================================

    screen = Screen()
    
    # handlers initialization
    home_page = HomePage()
    profile = Profile()
        
    # ======================================================================================================================================
   
    # app initialization
    app = QApplication(sys.argv)
    
    app.setOrganizationName("Health Quester")
    app.setOrganizationDomain("Medical Services")
    
    engine = QQmlApplicationEngine()

    # ======================================================================================================================================
  
    # passing references to QML
    ctx = engine.rootContext()
    ctx.setContextProperty('ref_icon', Config.Icons)
    ctx.setContextProperty('ref_screen', screen)
    ctx.setContextProperty('ref_home_page', home_page)
    ctx.setContextProperty('ref_profile', profile)
    ctx.setContextProperty('ref_sq_model', sq_model)
    ctx.setContextProperty('ref_query_model', query_model)
    ctx.setContextProperty('ref_report_model', report_model)

    # load qml app
    engine.load('ui/main.qml')
    
    # # these lines are used for debugging 
    # timer = QtCore.QTimer(interval=30000)
    # timer.timeout.connect(partial(lambda m: print(m.option_selected, m._option_id), home_page))
    # timer.timeout.connect(partial(lambda p: print(p.pressed, p.hovered), profile))
    # timer.timeout.connect(partial(lambda m: print(m.items), sq_model))
    # timer.timeout.connect(partial(lambda m: print(m.items), query_model))
    # timer.timeout.connect(partial(lambda m: m.setStatus(0, 1), report_model))
    # timer.timeout.connect(partial(lambda m: print(m.makeRequest()), sq_model))
    # timer.start()

    if not engine.rootObjects():

        return -1

    return app.exec()


if __name__ == '__main__':

    sys.exit(run_qml())
