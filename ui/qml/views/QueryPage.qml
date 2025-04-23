import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components
import "../views" as Views


Item {

    property string indicator: "queryPage"
   
    property real pageScale: 1.5
    property var goButton: goButton

    signal request()
    signal resetAll()

    // =======================================================================================================================================

    function checkAndUpdateStatus(index, card) 
    {
        /* returns true if status indicates that the specialization is out of service */

        var status = ref_query_model.getRole(index, "status");
                
        if (status == 1) {

            return false;
        }

        // case out of service [1] (i.e., the state = -1 indicates that this specialization service may be unavailable for a long time)
        else if (status === -1) {

            card.enabled = false;
            card.checkbox.checkState = Qt.Checked;
            card.btnIconUrl = ref_icon.out_of_service;
            card.btnIconColor = "gray";
            card.btnIconY = AppScreen.setScale(5 * query.pageScale);    
            card.btnText = "";
        }

        // case out of service [2] (i.e., the state = 0 indicates that this specialization service is temporarily unavailable)
        else if (status === 0) {

            card.enabled = false;
            card.checkbox.checkState = Qt.Checked;
            card.btnIconUrl = ref_icon.coming_soon;
            card.btnIconColor = "gray";
            card.btnIconY = AppScreen.setScale(5 * query.pageScale);    
            card.btnText = "";
        }

        return true;
    }

    // =======================================================================================================================================

    function getProfile(index) 
    {
        if (ref_query_model == null)  return null;
                
        return ref_query_model.getProfile(index);
    }
 
    // =======================================================================================================================================

    function isAnySelected() {

        if (ref_query_model == null)  return null;

        return ref_query_model.isAnySelected();
    }

    // =======================================================================================================================================

    function reloadProfile(visible) {

        if(active) {

            vProfileLoader.active = false;
        }

        var qml = "../views/VirtualProfile.qml"

        vProfileLoader.setSource(qml, {

            id: vprofile, visible: visible, 
            profile_index: panelRoot.last_active_index,
            profile: getProfile(panelRoot.last_active_index),
        });

        vProfileLoader.active = true;
    }

    // =======================================================================================================================================

    function resetProfile(visible) {

        var index = panelRoot.last_active_index;

        vprofile.resetProfile(index, getProfile(index));       
        vprofile.visible = visible;
    }
 
    // =======================================================================================================================================

 
    id: query
    
    // =======================================================================================================================================

    // Go Quester Button
    Views.SwipeButton {

        anchors.horizontalCenter: panelRoot.horizontalCenter

        id: goButton; btnWidth: 600 * query.pageScale; btnHeight: 50 * query.pageScale; onIconUrl: ref_icon.go
        y: panelRoot.y + panelRoot.height + AppScreen.setScale(25 * query.pageScale)
        visible: false

        onRun: {
            
            request();
        }
    }


    // =======================================================================================================================================

    property alias vprofile: vProfileLoader.item

    // Virtual Doctor Profile
    Loader {

        anchors.fill: parent
                
        id: vProfileLoader
        active: false

        Component.onCompleted: {

            // ...
        }

        Connections{

            enabled: true
            target: vprofile

            function onVisibleChanged() {

                goButton.visible = isAnySelected();
            }
        }
    }

    // Views.VirtualProfile {
        
    //     anchors.centerIn: parent
    //     id: vprofile
    //     window.visible: false
    //     profile_index: panelRoot.last_active_index
    //     profile: getProfile(panelRoot.last_active_index)

    //     window.onVisibleChanged: {
            
    //         goButton.visible = isAnySelected();
    //     }
    // }

    // =======================================================================================================================================

    // Panel
    Rectangle {
        
        // last active profile index
        property int last_active_index: 0

        anchors.centerIn: parent

        // width = 1200 + 40 left margin + 40 right margin
        // height = 600 + 40 left margin + 40 right margin
        id: panelRoot; width: AppScreen.setScale(1280 * query.pageScale); height: AppScreen.setScale(680 * query.pageScale)
        radius: AppScreen.setScale(100);

        border.width: AppScreen.setScale(10)
        border.color: "black"

        gradient: Gradient {
            GradientStop {position: 0.0; color: "#3F3697"}
            GradientStop {position: 1.0; color: "#344FA1"}
        }
                
        GridView {

            anchors.fill: parent
            anchors.margins: AppScreen.setScale(40 * query.pageScale)

            id: gridView
            model: ref_query_model
            clip: true

            cellWidth: AppScreen.setScale(300 * query.pageScale); cellHeight: AppScreen.setScale(300 * query.pageScale)

            delegate: Components.CheckBoxCard {

                id: card; btnWidth: 200 * query.pageScale; btnHeight: 200 * query.pageScale;
                
                btnText: title; btnIconUrl: iconUrl; btnIconColor: "transparent"; btnIconY: -10; enabled: true
                
                checkbox.checked: selected
                
                checkable: false
                
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
                    
                    panelRoot.last_active_index = index; 
                    resetProfile(true);
                }

                checkbox.onClicked: {

                    panelRoot.last_active_index = index;
                    resetProfile(true);
                }
            }
            
            boundsBehavior: Flickable.StopAtBounds
            
            ScrollBar.vertical: ScrollBar {id: scrollBar; active: false; x: parent.x + parent.width - 50}

            // ## these lines are necessary to avoid item life time destructuring (prevents checkbox being unchecked automatically)
            displayMarginBeginning: AppScreen.setScale(2000)
            displayMarginEnd: AppScreen.setScale(2000)
        }
    }

    // =======================================================================================================================================

    onResetAll: {

        reloadProfile(false);
        goButton.resetIndex();
        goButton.visible = false;
    }
}