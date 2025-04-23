import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components

Rectangle {
    
    property real btnWidth:  600
    property real btnHeight: 50
    property real btnRadius: 100

    property url offIconUrl: ref_icon.idea
    property url onIconUrl: ref_icon.xnext

    property int state: 1

    property alias swipe: swipeView
    
    signal run()
    signal resetIndex()

    id: rootItem; width: AppScreen.setScale(btnWidth); height: AppScreen.setScale(btnHeight); radius: AppScreen.setScale(btnRadius)
    
    gradient: Gradient {
        GradientStop {position: 0.0; color: "#3F3697"}
        GradientStop {position: 1.0; color: "#344FA1"}
    }

    SwipeView {

        id: swipeView
        currentIndex: 1
        
        width: parent.width; height: parent.height
        clip: true

        Components.IconButton {
                    
            id: offButton; btnWidth: 50; btnHeight: 50; btnIconUrl: rootItem.offIconUrl; btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 10;
            btnStartColor: "#019267"; btnEndColor: "#00C897";
        }

        Components.IconButton {
            
            id: onButton; btnWidth: 50; btnHeight: 50; btnIconUrl: rootItem.onIconUrl; btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 10;
        }

        onCurrentIndexChanged: {
            
            if(currentIndex === 0) {
                
                rootItem.state = 0;
                run();
            }
        }
    }

    onResetIndex: {
                
        if(rootItem.state === 0) {

            swipeView.currentIndex = 1;
            rootItem.state = 1;              
        }
    }
}