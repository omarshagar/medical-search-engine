import QtQuick 2.15
import QtQuick.Controls 2.15

import QtQuick.Layouts 1.1

import QtGraphicalEffects 1.8

import QtQuick.Controls.Material 2.2
import QtQuick.Controls.Material.impl 2.2

import "../../scripts/screen.js" as AppScreen

Item
{

    id: rootItem

    property color btnStartColor: "#3F3697"
    property color btnEndColor: "#344FA1"
    property real btnWidth:  250
    property real btnHeight: 200
    property url btnIconUrl: ""
    property real btnIconScale: 1.0
    property real btnIconY: 0.0
    property color btnIconColor: "white"
    property real btnRadius: 50

    property alias btn: btn
    property alias bg: btnBackground

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
            
            Image 
            {
                anchors.horizontalCenter: parent.horizontalCenter

                id: icon
                source: rootItem.btnIconUrl

                sourceSize.width: 0.75 * rootItem.width * rootItem.btnIconScale
                sourceSize.height: 0.75 * rootItem.height * rootItem.btnIconScale                              

                y: parent.y + parent.height / 2 - height / 2 + AppScreen.setScale(rootItem.btnIconY)
            }
            
            ColorOverlay {
                anchors.fill: icon
                source: icon
                color: rootItem.btnIconColor
            }
        }
    }

    Ripple {
        clipRadius: AppScreen.setScale(1)
        width: btn.width
        height: btn.height
        pressed: btn.pressed
        anchor: btn
        active: (btn.down || btn.visualFocus || btn.hovered)
        color: Material.rippleColor
    }
}