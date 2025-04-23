import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components
import "../views" as Views


Item {

    property string indicator: "reportHistoryPage"
    
    property real pageScale: 1.5

    signal resetAll()

    // =======================================================================================================================================

    function parseHeader(index)
    {
        if(ref_report_model == null) return []

        return ref_report_model.parseHeader(index);
    }

    // =======================================================================================================================================

    function updateHeader(index)
    {
        if(ref_report_model == null) return null

        return ref_report_model.updateHeader(index);
    }

    // =======================================================================================================================================

    function getReportProfile(index) 
    {
        if (ref_report_model === null)  return null;

        return ref_report_model.getReportProfile(index);
    }
 
    // =======================================================================================================================================

    function reloadProfile() {
        
        if(active) {

            vProfileLoader.active = false;
        }

        var qml = "../views/VirtualProfile.qml"

        vProfileLoader.setSource(qml, {

            id: vprofile, visible: false, 
            profile_index: panelRoot.last_active_index,
            profile: getReportProfile(panelRoot.last_active_index),
            hasOutputs: true,
        });

        vProfileLoader.active = true;
    }

    // =======================================================================================================================================

    function resetProfile(visible) {

        var index = panelRoot.last_active_index;

        vprofile.resetProfile(index, getReportProfile(index));       
        vprofile.visible = visible;
    }
 
    // =======================================================================================================================================

    id: report

    // =======================================================================================================================================

    property alias vprofile: vProfileLoader.item

    // Virtual Doctor Profile + Report
    Loader {

        anchors.fill: parent
                
        id: vProfileLoader
        active: false

        Component.onCompleted: {

            reloadProfile();
        }

        Connections{

            enabled: true
            target: vprofile
        }
    }

    // =======================================================================================================================================

    // Panel
    Rectangle {
        
        // last active profile index
        property int last_active_index: 0

        anchors.centerIn: parent

        // width = 1500 + 40 left margin + 40 right margin
        // height = 700 + 40 left margin + 40 right margin
        id: panelRoot; width: AppScreen.setScale(1580 * report.pageScale); height: AppScreen.setScale(780 * report.pageScale)
        radius: AppScreen.setScale(100);

        border.width: AppScreen.setScale(10)
        border.color: "black"

        gradient: Gradient {
            GradientStop {position: 0.0; color: "#3F3697"}
            GradientStop {position: 1.0; color: "#344FA1"}
        }
        
        // -------------------------------------------------------------------------------------------

        GridView {

            anchors.fill: parent
            anchors.margins: AppScreen.setScale(40 * report.pageScale)

            signal anyStatusChanged(int itemIndex)

            Component.onCompleted: {
                
                ref_report_model.anyStatusChanged.connect(gridView.anyStatusChanged);
            }

            id: gridView
            model: ref_report_model
            clip: true

            cellWidth: AppScreen.setScale(500 * report.pageScale); cellHeight: AppScreen.setScale(350 * report.pageScale)

            delegate: Views.ReportButton {

                property var self: card;

                id: card
                
                btnWidth: 450 * report.pageScale; btnHeight: 300 * report.pageScale
                labelWidth: 80 * report.pageScale; labelHeight: 40 * report.pageScale

                dataType: placeholderType
                dataUrl: placeholderUrl
                labels: parseHeader(index)

                state: status

                Component.onCompleted: {
                    // ...
                }

                // -------------------------------------------------------------------------------------------

                card.btn.onClicked: {

                    panelRoot.last_active_index = index;
                    resetProfile(true);
                }

                // -------------------------------------------------------------------------------------------

                // header update timer
                Timer {
                    
                    id: headerTimer

                    interval: 1000 
                    running: true 
                    repeat: true
                    
                    onTriggered: {

                        var state = updateHeader(index);
                                                
                        if(state == null) return;

                        labels = state.labels;

                        if(state.fixed) {
                            
                            running = false;
                            repeat = false;
                            return;
                        }
                    }
                }
                
                // -------------------------------------------------------------------------------------------

                // status update timer
                Timer {
                    
                    id: statusTimer

                    interval: 2000 
                    running: true 
                    repeat: true
                    
                    onTriggered: {

                        // .... ?
                        updateState(status);
                    }
                } 

                // -------------------------------------------------------------------------------------------
            }
            
            onAnyStatusChanged: {
                                                
                panelRoot.last_active_index = itemIndex;
            }

            boundsBehavior: Flickable.StopAtBounds
            
            ScrollBar.vertical: ScrollBar {id: scrollBar; active: false; x: parent.x + parent.width - 50}

            // ## these lines are necessary to avoid item life time destructuring (prevents checkbox being unchecked automatically)
            displayMarginBeginning: AppScreen.setScale(2000)
            displayMarginEnd: AppScreen.setScale(2000)
        }
    }


    // =======================================================================================================================================

    onResetAll: {
       
        reloadProfile();
    }
}