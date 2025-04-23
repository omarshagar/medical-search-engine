import QtQuick 2.15

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components

Item {
    
    property var dataUrl: ref_icon.output
    property var dataType: "image"

    property int dataIndex: 0

    property real btnWidth: 300
    property real btnHeight: 200

    property real labelWidth: 150
    property real labelHeight: 40

    property var labels: []
    
    property var toolbarLabels: ["next", "previous"]

    property alias card: dataviewer
    property alias toolbar: toolbar

    signal interaction()
    signal next()
    signal previous()
    signal showUrl()

    id: rootItem; width: AppScreen.setScale(btnWidth); height: AppScreen.setScale(btnHeight)

    // ==================================================================================================================================

    // Upload Button & DataViewer
    Components.MultimediaDataViewer {
        
        anchors.centerIn: parent
        
        id: dataviewer

        dataType: rootItem.dataType
        dataUrl: rootItem.dataUrl

        viewWidth: rootItem.btnWidth; viewHeight: rootItem.btnHeight; displayScale: 0.75;
        displayOverlayColor: "white"; itemY: 10; bg.border.color: "gray"

        btn.onClicked: {
            
            // notify
            interaction()
        }
    }

    // ==================================================================================================================================

    // Tags
    Components.Tags {
        
        anchors.top: parent.top
        anchors.bottomMargin: AppScreen.setScale(20)
        anchors.topMargin: AppScreen.setScale(20)
        anchors.horizontalCenter: parent.horizontalCenter

        id: tags
        
        labelWidth: rootItem.labelWidth
        labelHeight: rootItem.labelHeight

        viewCount: 3
        labels: rootItem.labels

        labelStartColor: "#7868E6"; labelEndColor: "#7868E6"
    }
    
    // ==================================================================================================================================

    // Toolbar
    Components.Tags {
    
        anchors.top: parent.bottom
        anchors.topMargin: AppScreen.setScale(20)
        anchors.bottomMargin: AppScreen.setScale(20)
        anchors.horizontalCenter: parent.horizontalCenter

        property int index: 0

        id: toolbar

        labelWidth: rootItem.labelWidth - 5
        labelHeight: rootItem.labelHeight - 5

        viewCount: 3
        labels: rootItem.toolbarLabels

        labelStartColor: "#7900FF"; labelEndColor: "#5800FF"
        
        visible: true

        onClicked: {
            
            // notify
            interaction()

            if(label === "next") {
                next();
            }

            else if(label === "previous") {
                previous();
            }

            else if(label === "show url") {
                showUrl();
            }
        }
    }
}
