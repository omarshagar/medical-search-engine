import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components

Item {

    // ==================================================================================================================================
    function checkStateAndUpdate(state)
    {
        if(state === 0) {

            enabled = false;
            busyIndicator.running = true;

            card.dataUrl = ref_icon.coming_soon;
            card.displayOverlayColor = "gray"

            tags.bgStartColor = "gray";
            tags.bgEndColor = "gray";

            tags.labelStartColor = "#413F42";
            tags.labelEndColor = "#413F42";
        }

        else {

            enabled = true;
            busyIndicator.running = false;

            card.dataUrl = rootItem.dataUrl;
            card.displayOverlayColor = "transparent"

            tags.bgStartColor = "#A2D2FF";
            tags.bgEndColor = "#A2D2FF";

            tags.labelStartColor = "#7868E6";
            tags.labelEndColor = "#7868E6";

        }
    }


    // ==================================================================================================================================

    property var dataUrl: ref_icon.missing
    property var dataType: "image"

    property real btnWidth: 300
    property real btnHeight: 200

    property real labelWidth: 100
    property real labelHeight: 40
    
    property var labels: []
    
    property int state: -1

    property alias card: card
    property alias busyIndicator: busyIndicator

    signal updateState(int state)

    id: rootItem; width: AppScreen.setScale(btnWidth); height: AppScreen.setScale(btnHeight)

    // ==================================================================================================================================

    Components.MultimediaDataViewer {
                
        id: card; 
        viewWidth: rootItem.btnWidth
        viewHeight: rootItem.btnHeight 
        dataType: rootItem.dataType
        dataUrl: rootItem.dataUrl
        displayScale: 0.75
        itemY: 10.0
        displayOverlayColor: "transparent"

        bg.border.color: "gray"     
    }

    // ==================================================================================================================================

    // Tags
    Components.Tags {
        
        // anchors.top: parent.top
        // anchors.bottomMargin: AppScreen.setScale(20)
        // anchors.topMargin: AppScreen.setScale(20)
        anchors.horizontalCenter: parent.horizontalCenter

        id: tags
        
        labelWidth: rootItem.labelWidth
        labelHeight: rootItem.labelHeight

        viewCount: 5
        labels: rootItem.labels

        labelStartColor: "#7868E6"; labelEndColor: "#7868E6"

        y: card.y + AppScreen.setScale(20)
    }


    // ==================================================================================================================================

    BusyIndicator { 
        
        id: busyIndicator

        anchors.centerIn: parent; 

        running: false
    }
    
    // ==================================================================================================================================

    onUpdateState: {
    
        checkStateAndUpdate(state);
    }

    // ==================================================================================================================================

    Component.onCompleted: {
        
        updateState(state);
    }
}
