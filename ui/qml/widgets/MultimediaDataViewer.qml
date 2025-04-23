import QtQuick 2.15
import QtQuick.Controls 2.15

import QtQuick.Layouts 1.1

import QtQuick.Controls.Material 2.2
import QtQuick.Controls.Material.impl 2.2

import "../../scripts/screen.js" as AppScreen

Item
{
    function getViewSrc(dataType)
    {
        if(dataType === "image") return "../widgets/_dataview/Image.qml";
        else return null;
    }

    // ===================================================================

    id: rootItem

    property string dataType
    property url dataUrl

    property color viewStartColor: "#3F3697"
    property color viewEndColor: "#344FA1"
    property real viewWidth:  250
    property real viewHeight: 200
    property real viewRadius: 50
    
    property real itemX: 0.0
    property real itemY: 0.0

    property real displayScale: 1.0
    property color displayOverlayColor: "transparent"

    property alias btn: btn
    property alias bg: btnBackground

    width: AppScreen.setScale(rootItem.viewWidth); height: AppScreen.setScale(rootItem.viewHeight)

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

                radius: AppScreen.setScale(rootItem.viewRadius)

                gradient: Gradient {
                    GradientStop {position: 0.0; color: rootItem.viewStartColor}
                    GradientStop {position: 1.0; color: rootItem.viewEndColor}
                }
            }
            
            Loader {
                
                anchors.centerIn: parent
                
                id: dataLoader
                
                Component.onCompleted: {
                    
                    var qml_src = getViewSrc(rootItem.dataType);
                    
                    if(qml_src === null) return;

                    setSource(qml_src, {id: data, viewer: rootItem});
                }
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