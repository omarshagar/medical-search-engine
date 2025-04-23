import QtQuick 2.15
import QtQuick.Controls 2.15

import QtQuick.Layouts 1.1

import QtGraphicalEffects 1.8

import QtQuick.Controls.Material 2.2
import QtQuick.Controls.Material.impl 2.2

import "../../scripts/screen.js" as AppScreen

/*
 * Modifying this widget would affect the following widgets:
 *  - Tags.qml 
 */

Item
{

    id: rootItem

    property color btnStartColor: "#3F3697"
    property color btnEndColor: "#344FA1"
    property real btnWidth:  250
    property real btnHeight: 200
    property string btnText: ""
    property color btnTextColor: "white"
    property real btnRadius: 50
    
    property real btnFontScale: 1.0
    property bool centered: true

    property bool rippleEnabled: true

    property alias btn: btn
    property alias bg: btnBackground
    property alias label: label
    
    width: AppScreen.setScale(rootItem.btnWidth); height: AppScreen.setScale(rootItem.btnHeight)

    Rectangle {

        anchors.fill: parent
            
        id: bg
        
        color: "transparent"

        Button 
        {
            anchors.fill: parent

            id: btn
            width: rootItem.width; height: 0.75 * rootItem.height
            hoverEnabled: true
            opacity: hovered ? 0.95 : 1.0

            background: Rectangle 
            {
                id: btnBackground

                radius: AppScreen.setScale(rootItem.btnRadius)

                gradient: Gradient {
                    GradientStop {position: 0.0; color: rootItem.btnStartColor}
                    GradientStop {position: 1.0; color: rootItem.btnEndColor}
                }
            }

            Text 
            {        
                anchors.centerIn: rootItem.centered ? parent : null

                id: label
                text: qsTr(rootItem.btnText)
                color: rootItem.btnTextColor
                font.pixelSize: ((0.095 * rootItem.width + 0.095 * rootItem.height) / 2) * AppScreen.setFontScale(rootItem.btnFontScale)
                font.bold: true    
            }
        }
    }

    Ripple {
        
        clipRadius: AppScreen.setScale(1)
        width: btn.width
        height: btn.height
        pressed: btn.pressed
        anchor: btn
        active: (btn.down || btn.visualFocus || btn.hovered) && rootItem.rippleEnabled
        color: Material.rippleColor
    }
}