import QtQuick 2.15
import QtQuick.Controls 2.15

import QtGraphicalEffects 1.8

import "../../../scripts/screen.js" as AppScreen

Item {
    
    property var viewer

    width: 0.75 * viewer.width * viewer.displayScale
    height: 0.75 * viewer.height * viewer.displayScale 

    Image 
    {
        anchors.horizontalCenter: parent.horizontalCenter

        id: indicator

        source: viewer.dataUrl

        sourceSize.width: parent.width
        sourceSize.height: parent.height
        
        y: parent.y + AppScreen.setScale(viewer.itemY + 25)
    }

    ColorOverlay {
        anchors.fill: indicator
        source: indicator
        color: viewer.displayOverlayColor
    }
}
