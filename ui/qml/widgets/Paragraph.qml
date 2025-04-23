import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components

Rectangle {
    

    property real pWidth: 250
    property real pHeight: 100
    
    property real bgRadius: 10
    property color bgStartColor: "#7900FF"
    property color bgEndColor: "#7900FF"
    
    property bool centered: false

    property alias header: header
    property alias paragraph: paragraph

    id: rootItem
    width: AppScreen.setScale(pWidth + 50)
    height: AppScreen.setScale(pHeight + 30)
    radius: AppScreen.setScale(bgRadius)
    clip: true

    gradient: Gradient {

        GradientStop {position: 0.0; color: rootItem.bgStartColor}
        GradientStop {position: 1.0; color: rootItem.bgEndColor}
    }

    Components.TextButton {
        
        id: header

        parent: rootItem.parent   
        anchors.left: rootItem.left
        
        btnWidth: 100 
        btnHeight: 50
        btnFontScale: 2.5
        btnText: ""; visible: false

        y: rootItem.y - height - AppScreen.setScale(10)
    }

    Flickable {

        anchors.centerIn: parent

        id: view; width: AppScreen.setScale(rootItem.pWidth); height: AppScreen.setScale(rootItem.pHeight)

        Label {
            
            id: paragraph

            width: AppScreen.setScale(rootItem.pWidth)
            text: ""
            
            font.pixelSize: AppScreen.setFontScale((0.095 * rootItem.width + 0.095 * rootItem.height) / 2)
            color: "white"

            wrapMode: Text.Wrap
            renderType: Text.NativeRendering

            Component.onCompleted: {
                
                if(centered) {
                    x = x + view.width / 2 - AppScreen.setScale(rootItem.pWidth) / 2;
                    y = y + view.height / 2.5;
                }
            }
        }

        contentWidth: paragraph.width
        contentHeight: paragraph.height + 1

        onImplicitHeightChanged: paragraph.update()

        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; width: 7}

        boundsBehavior: Flickable.StopAtBounds
    }
}