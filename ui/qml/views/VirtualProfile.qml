import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9
import QtQuick.Dialogs 1.2

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components
import "../views" as Views

Popup {

   anchors.centerIn: parent
   
   property real windowScale: 1.5

   // =======================================================================================================================================

   function getIconUrl() 
   {
      if(!profile) return ref_icon.missing;

      return ref_icon[profile.icon_name];
   }

   // ---------------------------------------------------------------

   function getTitle() 
   {
      if(!profile) return "";

      return profile.title;
   }

   // ---------------------------------------------------------------

   function getGreeting() 
   {
      if(!profile) return "";

      return profile.about.greeting;
   }

   // ---------------------------------------------------------------

   function getInfo() 
   {
      if(!profile) return "";

      return profile.about.info;
   }

   // ---------------------------------------------------------------

   function getSpecialization() 
   {
      if(!profile) return "";

      return profile.about.specialization;
   }

   // ---------------------------------------------------------------


   function getInputSummary() 
   {
      if(!profile) return "";

      return profile.about.input_summary;
   }

   // ---------------------------------------------------------------

   function getOutputSummary() 
   {
      if(!profile) return "";

      return profile.about.output_summary;
   }

   // ---------------------------------------------------------------

   function getNotes() 
   {
      if(!profile) return "";

      return profile.about.notes;
   }

 
   // =======================================================================================================================================

   function getInputsModel() {
      
      if(!profile) return [];

      return profile.inputs_model;
   }
   
   // =======================================================================================================================================

   function getOutputsModel() {
      
      if(!profile) return [];
      
      return profile.outputs_model;
   }

   // =======================================================================================================================================

   function setView(viewRoot, viewId) {
      
      function _setVisible(view, state) {

         for (var i=0; i<view.length; i++) {
            
            view[i].visible = state;
         }
      }

      var views = [viewRoot.a_view, viewRoot.b_view, viewRoot.c_view, viewRoot.d_view]

      for(var i=0; i<views.length; i++) {
         
         if(viewId == i) {

            _setVisible(views[i], true);
         }
         
         else {
         
            _setVisible(views[i], false);
         }
      }
   }


    // =======================================================================================================================================
   
   function setDialogueActive(loader_info, tags) {
            
      if(!loader_info) return;

      fileDialog.title = `Please upload a file based on the following tags : ${tags}`;
      fileDialog.selectMultiple =  (loader_info.max_count != 1);
      fileDialog.nameFilters = [`${loader_info.type} files (${loader_info.filters.join(' ')})`, "All files (*)" ];

      fileDialog.visible = true;
   }

   // =======================================================================================================================================
    
   function setData(inputs_model, fileUrls) {

      var state = inputs_model.setData(inputs_model.activeIndex, fileUrls);
      
      if(state <= 0) {
            
         var component = Qt.createComponent("../widgets/PopupMessage.qml");
         var object = component.createObject(bg);
         
         object.msgDuration = 8;
         object.msgText = `The number of loaded files exceeded the current supported limit, there are ${fileUrls.length} files that have been ignored`

         return false;
      }

      return true;
   }

   // =======================================================================================================================================
   
   function resetInputState(inputs) {
      
      var index = inputs.model.activeIndex;
      var state = inputs.model.columnCount(index);
      
      if(state !== 0) {
         return;
      }

      var input_button = inputs.activeButton;

      if(input_button === null) return;

      input_button.dataIndex = 0;
      input_button.card.dataType = "image";
      input_button.card.dataUrl = ref_icon.upload_input;
      input_button.card.displayOverlayColor = "white";      
   }

   // =======================================================================================================================================

   function resetDataViewState(inputs) {

      var index = inputs.model.activeIndex;
      var input_button = inputs.activeButton;

      var state = inputs.model.columnCount(index);

      if(input_button === null || state === 0) return;

      input_button.dataIndex = 0;
      input_button.card.dataType = "image";
      input_button.card.dataUrl = inputs.model.getColumn(index, input_button.dataIndex);
      input_button.card.displayOverlayColor = "transparent";
   }

   // =======================================================================================================================================
   function nextDataView(inputs) {

      var index = inputs.model.activeIndex;
      var state = inputs.model.columnCount(index);
      
      if(state === 0) {

         return;
      }

      var input_button = inputs.activeButton;

      input_button.dataIndex = (input_button.dataIndex + 1) % state;      
      input_button.card.dataUrl = inputs.model.getColumn(index, input_button.dataIndex);
   }

   // =======================================================================================================================================

   function previousDataView(inputs) {

      var index = inputs.model.activeIndex;
      var state = inputs.model.columnCount(index);

      if(state === 0) {
         return;
      }

      var input_button = inputs.activeButton;

      input_button.dataIndex = (input_button.dataIndex + state - 1) % state;
      input_button.card.dataUrl = inputs.model.getColumn(index, input_button.dataIndex);
   }

   // =======================================================================================================================================

   function popupShowUrl(inputs) {

      var index = inputs.model.activeIndex;
      var input_button = inputs.activeButton;

      var component = Qt.createComponent("../widgets/PopupMessage.qml");
      var object = component.createObject(bg);
      
      object.msgDuration = 10;
      object.msgStartColor = "#252A34";
      object.msgEndColor = "#393E46";
      object.msgText = inputs.model.getPath(index, input_button.dataIndex);
   }

   // =======================================================================================================================================

   function onResetProfileUpdate(profile_index, profile) {

      console.log("onResetProfileUpdate");

      rootItem.profile_index = profile_index;
      rootItem.profile = profile;
      
      inputs.model.columnChanged.connect(inputs.columnChanged);
      ref_report_model.outputsReady.connect(outputs.outputsReady);
   }

   // =======================================================================================================================================

    property var profile_index: null
    property var profile: null
    
    property bool hasOutputs: false
    
    property real windowWidth: 960
    property real windowHeight: 640

    property alias window: rootItem

    signal resetProfile(var profile_index, var profile)

    Component.onCompleted: {
       
       resetProfile.connect(onResetProfileUpdate);
    }

    topPadding: AppScreen.setScale(0)
    bottomPadding: AppScreen.setScale(0)
    leftPadding: AppScreen.setScale(0)
    rightPadding: AppScreen.setScale(0)

    background: Rectangle {
        
        gradient: Gradient {
        
            GradientStop {position: 0.0; color: "#3F3697"}
            GradientStop {position: 1.0; color: "#344FA1"}
        }

        border.color: "white"
        border.width: AppScreen.setScale(0 * rootItem.windowScale)
    }

    id: rootItem; 
    
    width: AppScreen.setScale(rootItem.windowWidth * rootItem.windowScale)
    height: AppScreen.setScale(rootItem.windowHeight * rootItem.windowScale)
    
    visible: true;

    modal: true
    focus: true

    Rectangle {

        property int viewId: 0

        property var a_view: [card, greeting, info, notes]
        property var b_view: [input_summary, output_summary]
        property var c_view: [inputs]
        property var d_view: [outputs]

        anchors.fill: parent
        
        id: bg
      
        gradient: Gradient {
        
            GradientStop {position: 0.0; color: "#3F3697"}
            GradientStop {position: 1.0; color: "#344FA1"}
        }
      
      // [1st] View ===============================================================================================================================================

      // Icon & Title
      Components.ButtonCard {
         
         anchors.top: parent.top
         anchors.left: parent.left
         
         anchors.margins: AppScreen.setScale(10 * rootItem.windowScale)

         id: card; 
         btnWidth: 150 * rootItem.windowScale
         btnHeight: 150 * rootItem.windowScale
         btnRadius: 10
         btnText: getTitle(); btnIconUrl: getIconUrl()
         btnIconColor: "transparent"; btnIconY: -10; enabled: false
      }

      // ----------------------------------------------------------------------------------------------------------------------

      // Greeting
      Components.Paragraph {
         
         id: greeting;
         
         anchors.left: card.right
         anchors.margins: AppScreen.setScale(10)

         pWidth: rootItem.windowWidth * rootItem.windowScale - AppScreen.unscale(card.width) - 100 * rootItem.windowScale
         pHeight: AppScreen.unscale(card.height) - 50 * rootItem.windowScale
         bgRadius: 10; 

         y: card.y

         paragraph.text: getGreeting()
         paragraph.color: "white"
         paragraph.font.bold: false
         
         centered: true

         bgStartColor: "#3F3697"; bgEndColor: "#344FA1"
      }

      // ----------------------------------------------------------------------------------------------------------------------

      // Info
      Components.Paragraph {
         
         anchors.left: parent.left
         anchors.top: card.bottom
         
         anchors.topMargin: AppScreen.setScale(150)
         anchors.leftMargin: AppScreen.setScale(10 * rootItem.windowScale)

         header.width: AppScreen.setScale(200)
         header.height: AppScreen.setScale(80)

         id: info;

         pWidth: AppScreen.unscale(card.width) + AppScreen.unscale(greeting.width) - 40
         pHeight: AppScreen.unscale(card.height) - 50 * rootItem.windowScale

         bgRadius: 10; 

         paragraph.text: getInfo()
         paragraph.color: "white"
         paragraph.font.bold: false

         centered: true

         bgStartColor: "#3F3697"; bgEndColor: "#344FA1"

         header.btnText: getSpecialization()
         header.visible: visible
      }


      // Notes
      Components.Paragraph {
         
         anchors.left: parent.left
         anchors.top: info.bottom
         
         anchors.topMargin: AppScreen.setScale(150)
         anchors.leftMargin: AppScreen.setScale(10 * rootItem.windowScale)

         header.width: AppScreen.setScale(200)
         header.height: AppScreen.setScale(80)

         id: notes;

         pWidth: AppScreen.unscale(card.width) + AppScreen.unscale(greeting.width) - AppScreen.unscale(back.width) - 40
         pHeight: AppScreen.unscale(card.height) - 60 * rootItem.windowScale

         bgRadius: 10;
         
         paragraph.text: getNotes()
         paragraph.color: "white"
         paragraph.font.bold: false
         
         bgStartColor: "#3F3697"; bgEndColor: "#344FA1"
 
         header.btnText: "Note"
         header.visible: visible

         centered: true
      }


      // [2nd] View ===============================================================================================================================================

      // Input Summary
      Components.Paragraph {
         
         anchors.horizontalCenter: parent.horizontalCenter
         
         id: input_summary;
         
         header.width: AppScreen.setScale(150)
         header.height: AppScreen.setScale(80)

         pWidth: (rootItem.windowWidth - 200) * rootItem.windowScale
         pHeight: (rootItem.windowHeight * 0.25) * rootItem.windowScale

         bgRadius: 10
         visible: false
         
         y: header.height + AppScreen.setScale(25)

         paragraph.text: getInputSummary()
         paragraph.color: "white"
         paragraph.font.bold: false
         
         bgStartColor: "#3F3697"; bgEndColor: "#344FA1"

         header.btnText: "Input Summary"
         header.visible: visible

         centered: true
      }

      // ----------------------------------------------------------------------------------------------------------------------

      // Output Summary
      Components.Paragraph {
   
         anchors.horizontalCenter: parent.horizontalCenter

         id: output_summary;
         
         header.width: AppScreen.setScale(150)
         header.height: AppScreen.setScale(80)

         pWidth: (rootItem.windowWidth - 200) * rootItem.windowScale
         pHeight: (rootItem.windowHeight * 0.25) * rootItem.windowScale
         bgRadius: 10
         visible: false
         
         y: input_summary.y + input_summary.height + header.height + AppScreen.setScale(50)

         paragraph.text: getOutputSummary()
         paragraph.color: "white"
         paragraph.font.bold: false
         
         bgStartColor: "#3F3697"; bgEndColor: "#344FA1"

         header.btnText: "Output Summary"
         header.visible: visible

         centered: true
      }


      // [3rd] View ===============================================================================================================================================
      
      FileDialog {
                 
         id: fileDialog
         folder: shortcuts.home
        
         onAccepted: {

            inputs.ready(fileDialog.fileUrls);
         }

         visible: false
      }

      // Inputs
      GridView {
         
         property var activeButton: null

         signal columnChanged(int oldCount, bool append)
         signal ready(var fileUrls)

         anchors.fill: parent
         anchors.margins: AppScreen.setScale(40 * rootItem.windowScale)

         id: inputs; visible: false
         
         // set InputModel
         model: getInputsModel()

         clip: true

         cellWidth: AppScreen.setScale(440 * rootItem.windowScale); cellHeight: AppScreen.setScale(280 * rootItem.windowScale)

         delegate: Views.InputButton {
                        
            id: input_button; labels: tags
            btnWidth: 350 * rootItem.windowScale
            btnHeight: 210 * rootItem.windowScale

            toolbarLabels: rootItem.hasOutputs === true ? ["next", "previous"] : ["next", "previous", "remove", "show url"]
            
            // If status != InputStatus.Free
            toolbar.visible: (status !== 0) | (rootItem.hasOutputs)

            Component.onCompleted: {
               
               inputs.model.activeIndex = index;
               inputs.activeButton = input_button;
   
               if(status !== 0 || rootItem.hasOutputs) {
                  
                  resetDataViewState(inputs);
               }

               else {

                  resetInputState(inputs);
               }
            }

            onClicked: {

               if(!rootItem.hasOutputs) {
                                    
                  setDialogueActive(loader_info, tags);
               }
            }

            onInteraction: {
               
               inputs.model.activeIndex = index;
               inputs.activeButton = input_button;
            }

            onNext: {

               nextDataView(inputs);
            }

            onPrevious: {

               previousDataView(inputs);
            }

            onRemove: {
               
               inputs.model.removeColumn(index, dataIndex);
            }

            onShowUrl: {

               popupShowUrl(inputs);
            }
         }

         onColumnChanged: {

            var index = inputs.model.activeIndex;
            var state = inputs.model.columnCount(index);
            
            console.log(append, oldCount, state);
            
            // push
            if(append === true) {
               
               if(oldCount === 0) {

                  resetDataViewState(inputs);
               }

               else {

                   inputs.activeButton.next();
               }
            }

            // pop
            else {
               
               if(state === 0) {

                  resetInputState(inputs);
               }
                  
               else {

                  inputs.activeButton.previous();
               }
            }

             // update profile state (query model)
            ref_query_model.checkAndUpdateSelected(rootItem.profile_index);
         }

         onReady: {

            var state = setData(model, fileUrls);
         }

         boundsBehavior: Flickable.StopAtBounds
         
         ScrollBar.vertical: ScrollBar {id: inputScrollBar; active: false; policy: ScrollBar.AlwaysOn}

         // ## these lines are necessary to avoid item life time destructuring (prevents checkbox being unchecked automatically)
         displayMarginBeginning: AppScreen.setScale(1000)
         displayMarginEnd: AppScreen.setScale(1000)
      }
      
      // [4th] View ===============================================================================================================================================


      // Outputs
      GridView {

         property var activeButton: null

         anchors.fill: parent
         anchors.margins: AppScreen.setScale(40 * rootItem.windowScale)

         id: outputs; visible: false

         signal outputsReady()

         model: getOutputsModel()

         clip: true

         cellWidth: AppScreen.setScale(440 * rootItem.windowScale); cellHeight: AppScreen.setScale(280 * rootItem.windowScale)

         delegate: Views.OutputButton {
            
            id: output_button; labels: tags
            btnWidth: 350 * rootItem.windowScale
            btnHeight: 210 * rootItem.windowScale

            Component.onCompleted: {

               outputs.model.activeIndex = index;
               outputs.activeButton = output_button;
                        
               if(status !== 0 || rootItem.hasOutputs) {

                  resetDataViewState(outputs);
               }

               else {
                  
                  resetInputState(outputs);
               }
            }

            onInteraction: {
               
               outputs.model.activeIndex = index;
               outputs.activeButton = output_button;
            }

            onNext: {

               nextDataView(outputs);
            }

            onPrevious: {

               previousDataView(outputs);
            }
         }

         onOutputsReady: {
            
            // ...
         }

         boundsBehavior: Flickable.StopAtBounds
         
         ScrollBar.vertical: ScrollBar {id: outputScrollBar; active: false; policy: ScrollBar.AlwaysOn}

         // ## these lines are necessary to avoid item life time destructuring (prevents checkbox being unchecked automatically)
         displayMarginBeginning: AppScreen.setScale(1000)
         displayMarginEnd: AppScreen.setScale(1000)
      }

      // ============================================================================================================================================================
      
      // Next Button
      Components.IconButton {
         
         anchors.right: parent.right
         anchors.bottom: parent.bottom
         anchors.margins: AppScreen.setScale(10 * rootItem.windowScale)

         id: next
         btnWidth: 50 * rootItem.windowScale
         btnHeight: 50 * rootItem.windowScale 
         btnIconUrl: ref_icon.next; 
         btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 10;
         
         btn.onClicked: {

            parent.viewId += 1;            
            setView(parent, parent.viewId);
            back.visible = true;
            next.visible = (parent.viewId != 2 && !rootItem.hasOutputs) | (parent.viewId != 3 && rootItem.hasOutputs);
         } 
      }

      // Back Button
      Components.IconButton {
         
         anchors.left: parent.left
         anchors.bottom: parent.bottom
         anchors.margins: AppScreen.setScale(10 * rootItem.windowScale)

         id: back
         btnWidth: 50 * rootItem.windowScale
         btnHeight: 50 * rootItem.windowScale 
         btnIconUrl: ref_icon.back
         btnIconScale: 1.0; btnIconY: 0.0; btnRadius: 10; visible: false;
         
         btn.onClicked: {
            parent.viewId -= 1;
            setView(parent, parent.viewId);
            back.visible = (parent.viewId != 0);
            next.visible = (parent.viewId != 2) | (parent.viewId != 3 && rootItem.hasOutputs);
         } 
      }
   }

   // reset states
   onVisibleChanged: {
   
      bg.viewId = 0;      
      
      setView(bg, bg.viewId);
      
      back.visible = false;
      next.visible = true;

      inputs.positionViewAtBeginning();
      outputs.positionViewAtBeginning();
   }
}