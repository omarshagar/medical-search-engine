import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen
import "../../scripts/popup.js" as PopupMsg

import "../widgets" as Components

Item {
    
    property string indicator: "homePage"

    property real pageScale: 1.0

    signal autoQuestClicked()
    signal specializedQuestClicked()
    signal questBotClicked()
    signal reportHistoryClicked()
    signal supportTeamClicked()
    signal questCalendarClicked()
    signal faqClicked()
    signal helpClicked()

    // ==============================================================================================================================

    id: home

    Grid {

        anchors.centerIn: parent

        id: options
        rows: 2
        columns: 4
        spacing: AppScreen.setScale(16 * home.pageScale)
        
        // first row
        Components.ButtonCard {

            id: autoquest; btnIconUrl: ref_icon.autoquest; btnText: "Auto Quest"; btnIconScale: 1.0; btnIconY: 0.0; 

            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale

            btn.onClicked: {
                
                autoQuestClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "autoquest";

                PopupMsg.showFeatureNotAvailableMsg(autoquest, 0.75);
            }
        }

        Components.ButtonCard {

            id: specializedQuest;  btnIconUrl: ref_icon.specializedquest; btnText: "Specialized Quest"; btnIconScale: 0.9; btnIconY: 10.0

            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale

            btn.onClicked: {
                
                specializedQuestClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "specializedQuest";
            }
        }

        Components.ButtonCard {

            id: questbot; btnIconUrl: ref_icon.questbot; btnText: "Quest Bot"; btnIconScale: 1.0; btnIconY: 0.0
            
            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale
        
            btn.onClicked: {   

                questBotClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "questBot";

                PopupMsg.showFeatureNotAvailableMsg(questbot, 0.75);
            }
        }
        
        Components.ButtonCard {
            
            id: reportHistory; btnIconUrl: ref_icon.report; btnText: "Report History"; btnIconScale: 0.95; btnIconY: 5.0
            
            btn.onClicked: {   

                reportHistoryClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "reportHistory";
            }
        }

        // second row
        Components.ButtonCard {
            
            id: supportTeam

            btnIconUrl: ref_icon.supportteam; btnText: "Support Team"; btnIconScale: 1.0; btnIconY: 0.0

            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale

            btn.onClicked: {    

                supportTeamClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "supportTeam";

                PopupMsg.showFeatureNotAvailableMsg(supportTeam, 0.75, "This section is not yet available");
            }
        }
        
        Components.ButtonCard {
        
            id: questCalendar; btnIconUrl: ref_icon.questcalendar; btnText: "Quest Calendar"; btnIconScale: 1.0; btnIconY: 0.0
            
            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale

            btn.onClicked: {  
                
                questCalendarClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "questCalendar";

                PopupMsg.showFeatureNotAvailableMsg(questCalendar, 0.75);
            }
        }
        
        Components.ButtonCard {
            
            id: faq; btnIconUrl: ref_icon.faq; btnText: "FAQ"; btnIconScale: 0.9; btnIconY: 10.0

            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale

            btn.onClicked: {        

                faqClicked();

                ref_home_page.option_selected = true;
                ref_home_page.option_id = "faq";

                PopupMsg.showFeatureNotAvailableMsg(faq, 0.75, "This section is not yet available");
            }
        }
        
        Components.ButtonCard {
            
            id: help; btnIconUrl: ref_icon.help; btnText: "Ask For Help"; btnIconScale: 0.9; btnIconY: 5.0

            btnWidth: 400 * home.pageScale; btnHeight: 350 * home.pageScale

            btn.onClicked: {         

                helpClicked();
                   
                ref_home_page.option_selected = true;
                ref_home_page.option_id = "help";

                PopupMsg.showFeatureNotAvailableMsg(help, 0.75, "This section is not yet available");
            }
        }
    }
}