import QtQuick 2.15
import QtQuick.Controls 2.15

import QtQuick.Layouts 1.1

import QtGraphicalEffects 1.8

import QtQuick.Controls.Material 2.2
import QtQuick.Controls.Material.impl 2.2

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components

/*
 * Modifying this widget would affect the following widgets:
 *  - Paragraph.qml 
 */

Item {

    property real labelWidth: 75
    property real labelHeight: 25
    property real labelRadius: 100

    property color labelStartColor: "#3F3697"
    property color labelEndColor: "#344FA1"

    property real labelFontSize: 2

    property color labelTextColor: "white"
    
    property real labelSpacing: 2
    
    property real viewCount: 4

    property real bgWidthPadding: 26.5
    property real bgHeightPadding: 20

    property real bgRadius: 100
    
    property color bgStartColor: "#A2D2FF"
    property color bgEndColor: "#A2D2FF"
        
    property var labels: []
    
    signal clicked(var label)

    id: rootItem

    width: AppScreen.setScale(rootItem.labelWidth * rootItem.viewCount + rootItem.bgWidthPadding)
    height: AppScreen.setScale(rootItem.labelHeight + rootItem.bgHeightPadding)

    Rectangle {
        
        anchors.fill: parent

        id: bg; radius: AppScreen.setScale(rootItem.bgRadius)

        gradient: Gradient {

            GradientStop {position: 0.0; color: rootItem.bgStartColor}
            GradientStop {position: 1.0; color: rootItem.bgEndColor}
        }

        ListView {
                
            anchors.fill: parent
        
            anchors.margins: AppScreen.setScale(10)
            spacing: AppScreen.setScale(rootItem.labelSpacing)

            orientation: ListView.Horizontal

            id: listview
            model: labels.length
            clip: true

            delegate: Components.TextButton {
                
                id: tag
                btnWidth: rootItem.labelWidth
                btnHeight: rootItem.labelHeight
                btnRadius: rootItem.labelRadius
                btnTextColor: rootItem.labelTextColor
                btnText: labels[index]
                btnFontScale: 2.5
                btnStartColor: rootItem.labelStartColor
                btnEndColor: rootItem.labelEndColor
                
                btn.onClicked: {
                    
                    rootItem.clicked(labels[index]);    
                }
            }
            
            boundsBehavior: Flickable.StopAtBounds
            
            ScrollBar.horizontal: ScrollBar {

                id: scrollBar; active: false
                height: AppScreen.setScale(5)
                y: parent.y + parent.height / 2 - 1
            }
        }
    }
}