import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9
import QtQuick.Controls.Material 2.15
import QtGraphicalEffects 1.9
import  QtQuick.Controls.Styles 1.4
import QtQuick.Dialogs 1.2

import "scripts/screen.js" as AppScreen

import "qml/widgets" as Components
import "qml/views" as Views

Window {

    // ==========================================================================================================================================================
    
    property var queryPage: queryPageLoader.item
    property var reportHistoryPage: reportHistoryPageLoader.item

    // ===========================================================================================================================================================

    id: rootWindow
    visible: true
    width: 1800
    height: 900
    color: "#161616"
    title: "Health Quester"

    // ===========================================================================================================================================================

    onWidthChanged: {
        // ...
    }

    onHeightChanged: {
       // ...
    }

    // ===========================================================================================================================================================

    // Profile button, will never be removed or created twice, however being disabled and/or hidden when it is necessary
    Components.IconButton {

        anchors.top: parent.top
        anchors.right: parent.right
        anchors.rightMargin: AppScreen.setScale(15)
        anchors.topMargin: AppScreen.setScale(15)

        id: profile; btnWidth: 150; btnHeight: 150; btnIconUrl: ref_icon.profile; 
        btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 100; 

        btn.onClicked: {            
            ref_profile.pressed = true;
        }

        btn.onHoveredChanged: { 
            ref_profile.hovered = btn.hovered;   
        }
    }

    // ===========================================================================================================================================================


    // Back button option icon, will never be removed or created twice, however being disabled and/or hidden when it is necessary
    Components.IconButton {

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: AppScreen.setScale(15)
        anchors.topMargin: AppScreen.setScale(15)

        id: back; btnWidth: 150; btnHeight: 150; btnIconUrl: ref_icon.previous; 
        btnIconScale: 0.95; btnIconY: 0.0; btnRadius: 100; visible: (pagesView.depth > 1)

        btn.onClicked: {

            navigationHandler.navigate(null, false, 5, null);
        }
    }

    // ===========================================================================================================================================================

    BusyIndicator { 
        
        id: busyIndicator

        anchors.centerIn: parent; 

        running: false
    }

    Timer {
        
        property int maxCount: 2
        property int counter: -1

        property var currentPage: null
        property var previousPage: null

        property bool forward: false

        signal navigateForward()
        signal navigateBackward()

        signal navigate(var page, bool isForward, int sleepTime, var previous)
        signal remove(int index)

        id: navigationHandler

        onNavigateForward: {
            
            pagesView.push(currentPage);
        }

        onNavigateBackward: {
            
            pagesView.pop();
        }
        
        onNavigate: {

            currentPage = page;
            previousPage = previous;
            forward = isForward;
            interval = sleepTime;
            start();
        }

        onRemove: {

            interval = 0;

            var page = pagesView.get(index, StackView.DontLoad);

            if(page != null && index != pagesView.depth) {
                
                pagesView.pop(page, StackView.Immediate);
            }
        }

        interval: 0 
        running: false 
        repeat: true
        
        triggeredOnStart: {

            busyIndicator.running = running;
        }

        onTriggered: {
            
            counter += 1;

            if(counter == 2 && !pagesView.busy) {
                

                if(previousPage != null) {
                    
                    for(var i=0; i < pagesView.depth; i++) {

                        navigationHandler.remove(i);
                    }

                    pagesView.initialItem = previousPage;
                }

                if(forward === true) {
                 
                    navigateForward();
                }

                else {
                    
                    navigateBackward();
                }
                
                counter = -1;
                running = false;
            }            
        }
    }

    // ===========================================================================================================================================================

    StackView {

        anchors.fill: parent

        id: pagesView

        initialItem: signInPage

        // =============================================================================================

        // Sign-In: Page View
        Views.SignIn {
            
            id: signInPage
            visible: true

            onJoinAsGuest: {

                navigationHandler.navigate(homePage, true, 10, null);
            }
        }

        // =============================================================================================

        // Home: Page View
        Views.HomePage {

            id: homePage
            visible: false

            onSpecializedQuestClicked: {
                
                navigationHandler.navigate(specializedQuestPage, true, 10, null);
            }

            onReportHistoryClicked: {

                reportHistoryPageLoader.active = true;
                navigationHandler.navigate(reportHistoryPage, true, 10, null);
            }
        }

        // =============================================================================================

        // Specialized Quest: Page View
        Views.SpecializedQuestPage{
            
            id: specializedQuestPage
            visible: false

            Connections {

                enabled: true
                target: specializedQuestPage

                function onRequest() {

                    ref_sq_model.makeRequest();
                    queryPageLoader.active = true;

                    navigationHandler.navigate(queryPage, true, 100, null);
                }
            }
        }

        // =============================================================================================

        // Query Page
        Loader {
       
            id: queryPageLoader

            active: false
            // asynchronous: true

            Component.onCompleted: {
            
                var qml = "qml/views/QueryPage.qml"
            
                setSource(qml, {
                    id: queryPage, visible: false
                });

            }

            Connections{

                enabled: true
                target: queryPage

                function onRequest() {

                    ref_query_model.makeRequest();
                    reportHistoryPageLoader.active = true;

                    navigationHandler.navigate(reportHistoryPage, true, 100, homePage);
                }
            }
        }

        // =============================================================================================

        // Report History Page
        Loader {
            
            id: reportHistoryPageLoader

            active: false
            // asynchronous: true

            Component.onCompleted: {
                            
                var qml = "qml/views/ReportHistory.qml"
            
                setSource(qml, {
                    
                    id: reportHistoryPage, visible: false
                });
            }

            Connections{

                enabled: true
                target: reportHistoryPage

            }


            Connections {

                enabled: true
                target: pagesView
            }
        }

        // =============================================================================================


        onCurrentItemChanged: {
            
            if(currentItem.indicator === "specializedQuestPage") {
             
                specializedQuestPage.resetAll();
            }

            else if(currentItem.indicator === "queryPage") {
             
                queryPage.resetAll();
            }

            else if(currentItem.indicator === "reportHistoryPage") {
            
                reportHistoryPage.resetAll();
            }
        }
    }
}

