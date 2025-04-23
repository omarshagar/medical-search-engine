import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components
import "../views" as Views


Item {

    property string indicator: "specializedQuestPage"
   
    property real pageScale: 1.5

    property var runButton: runButton
    
    signal request()
    signal resetAll()
    
    // =======================================================================================================================================

    function checkAndUpdateStatus(index, card) 
    {
        /* returns true if status indicates that the specialization is out of service */

        var status = ref_sq_model.getRole(index, "status");
                
        if (status == 1) {

            return false;
        }

        // case out of service [1] (i.e., the state = -1 indicates that this specialization service may be unavailable for a long time)
        else if (status === -1) {

            card.enabled = false;
            card.checkbox.checkState = Qt.Checked;
            card.btnIconUrl = ref_icon.out_of_service;
            card.btnIconColor = "gray";
            card.btnText = "";
        }

        // case out of service [2] (i.e., the state = 0 indicates that this specialization service is temporarily unavailable)
        else if (status === 0) {

            card.enabled = false;
            card.checkbox.checkState = Qt.Checked;
            card.btnIconUrl = ref_icon.coming_soon;
            card.btnIconColor = "gray";
            card.btnText = "";
        }

        return true;
    }

    // =======================================================================================================================================
    
    function sq_next(panelRoot) {

        // as the next button has been clicked -> get the next view (childs)
        var state = ref_sq_model.next();
        
        // if user does not select any parent, create a popup message
        if(state === -1) {
            
            var component = Qt.createComponent("../widgets/PopupMessage.qml");
            var object = component.createObject(panelRoot);
            
            object.msgWidth *= specializedquest.pageScale;
            object.msgHeight *= specializedquest.pageScale;
            object.msgText = "You need to select at least one specialization to continue 🥲";

            return false;
        }

        // if there is no next view (all nodes are leaves), create a popup message
        else if(state === 0) {

            var component = Qt.createComponent("../widgets/PopupMessage.qml");
            var object = component.createObject(panelRoot);
            
            object.msgWidth *= specializedquest.pageScale;
            object.msgHeight *= specializedquest.pageScale;
            object.msgText = "There are not extra sub-specializations. Happy Questing! 🥸";
            
            return false;
        }

        return true;
    }

    // =======================================================================================================================================
    
    function sq_previous(panelRoot) {

        // as the previous button has been clicked -> get the previous view (parents)
        var state = ref_sq_model.previous();

        // if there is no previous
        if(state === 0) {
            
            // var component = Qt.createComponent("../widgets/PopupMessage.qml");
            // var object = component.createObject(panelRoot);
            
            // object.msgWidth *= specializedquest.pageScale;
            // object.msgHeight *= specializedquest.pageScale;
            // object.msgText = "Ah nice try 🥱, but there are a lot of things you can still do";

            return false;
        }

        return true;
    }

    // =======================================================================================================================================
    
    id: specializedquest

    // =======================================================================================================================================

    // Next Button
    Components.IconButton {
          
        id: next; btnWidth: 100 * specializedquest.pageScale; btnHeight: 100 * specializedquest.pageScale; 
        btnIconUrl: ref_icon.xnext; btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 10;
        x: panelRoot.x + panelRoot.width + btn.width - AppScreen.setScale(50 * specializedquest.pageScale)
        y: panelRoot.y + panelRoot.height / 2 - AppScreen.setScale(50 * specializedquest.pageScale)
        
        btn.onClicked: {

            if(sq_next(panelRoot)) {

                back.visible = true;
            }  
        } 
    }

    // =======================================================================================================================================

    // Previous Button
    Components.IconButton {
                
        id: back; btnWidth: 100 * specializedquest.pageScale; btnHeight: 100 * specializedquest.pageScale; 
        btnIconUrl: ref_icon.xback; btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 10; visible: false
        x: panelRoot.x - btn.width - AppScreen.setScale(50 * specializedquest.pageScale)
        y: panelRoot.y + panelRoot.height / 2 - AppScreen.setScale(50 * specializedquest.pageScale)
        

        btn.onClicked: {

            var success = sq_previous(panelRoot);

            if (ref_sq_model.isTop()) {
                visible = false;
            }
        }
    }

    // =======================================================================================================================================

    // Run Quester Button
    Views.SwipeButton {

        anchors.horizontalCenter: panelRoot.horizontalCenter

        id: runButton; btnWidth: 600 * specializedquest.pageScale; btnHeight: 50 * specializedquest.pageScale
        y: panelRoot.y + panelRoot.height + AppScreen.setScale(25 * specializedquest.pageScale)

        onRun: {

            request();
        }
    }

    // =======================================================================================================================================

    // BusyIndicator { 

    //     anchors.centerIn: panelRoot; 

    //     running: {
    //         if(ref_sq_model != null) 
    //             return ref_sq_model.loading; 
    //         else 
    //             return false;
    //     } 
    // }

    // =======================================================================================================================================

    // Panel
    Rectangle {
        
        anchors.centerIn: parent

        // width = 1200 + 40 left margin + 40 right margin
        // height = 600 + 40 left margin + 40 right margin
        id: panelRoot; width: AppScreen.setScale(1280 * specializedquest.pageScale)
        height: AppScreen.setScale(680 * specializedquest.pageScale); radius: AppScreen.setScale(100)

        border.width: AppScreen.setScale(10)
        border.color: "black"

        gradient: Gradient {
            GradientStop {position: 0.0; color: "#3F3697"}
            GradientStop {position: 1.0; color: "#344FA1"}
        }
                
        GridView {

            anchors.fill: parent
            anchors.margins: AppScreen.setScale(40 * specializedquest.pageScale)

            id: gridView
            model: ref_sq_model
            clip: true

            cellWidth: AppScreen.setScale(300 * specializedquest.pageScale)
            cellHeight: AppScreen.setScale(300 * specializedquest.pageScale)

            delegate: Components.CheckBoxCard {

                id: card; btnWidth: 200 * specializedquest.pageScale; btnHeight: 200 * specializedquest.pageScale;
                
                btnText: name; btnIconUrl: iconUrl; btnIconColor: "white"; enabled: true

                property var self: card;

                Component.onCompleted: {
                    
                    if(checkAndUpdateStatus(index, self)) {

                        return;
                    }
                   
                    // on load of a previously selected item
                    if(selected === true) {

                        checkbox.checkState = Qt.Checked;
                    }
                }

                btn.onClicked: {

                    // if the button has been clicked update selected state
                    ref_sq_model.nextCheckState(index, checkbox.checked);
                }

                checkbox.onClicked: {
                    
                    // if the checkbox has been  clicked update selected state
                    ref_sq_model.nextCheckState(index, checkbox.checked);
                }

            }
            
            boundsBehavior: Flickable.StopAtBounds
            
            ScrollBar.vertical: ScrollBar {
                
                id: scrollBar; active: false
            
                x: parent.x + parent.width - AppScreen.setScale(50 * specializedquest.pageScale)
            }

            // ## these lines are necessary to avoid item life time destructuring (prevents checkbox being unchecked automatically)
            displayMarginBeginning: AppScreen.setScale(1000)
            displayMarginEnd: AppScreen.setScale(1000)
        }
    }

    // =======================================================================================================================================
    
    onResetAll: {
        
        runButton.resetIndex();
    }
}