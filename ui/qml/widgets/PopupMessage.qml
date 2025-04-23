import QtQuick 2.15

import "../../scripts/screen.js" as AppScreen

Rectangle {

    anchors.centerIn: parent
    
    property real msgWidth: 500
    property real msgHeight: 100
    property real msgRadius: 100

    property color msgStartColor: "#525E75"
    property color msgEndColor: "#78938A"

    property string msgText: ""
    property color msgTextColor: "white"

    property real msgDuration: 5 // in seconds
    
    property real msgStartOpacity: 1.0

    id: rootItem

    width: AppScreen.setScale(rootItem.msgWidth); height: AppScreen.setScale(rootItem.msgHeight); 
    radius: AppScreen.setScale(rootItem.msgRadius); opacity: rootItem.msgStartOpacity

    Text 
    {           
        anchors.centerIn: parent

        id: msg
        width: rootItem.width - AppScreen.setScale(50)
        text: qsTr(rootItem.msgText)
        color: rootItem.msgTextColor
        font.bold: true
        wrapMode: Text.Wrap
        renderType: Text.NativeRendering
    }

    gradient: Gradient {
        
        GradientStop {position: 0.0; color: rootItem.msgStartColor}
        GradientStop {position: 1.0; color: rootItem.msgEndColor}
    }

    OpacityAnimator on opacity{

        from: rootItem.msgStartOpacity;
        to: 0;
        
        duration: 1000 * rootItem.msgDuration

        onRunningChanged: {

            if(rootItem.opacity === 0) {

                rootItem.destroy(); 
            }
        }
    }
}