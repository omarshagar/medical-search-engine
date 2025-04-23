import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

Item
{
    // --------------------------------------------------------------------------------------------------------------------------------------------------

    function checkAndUpdate()
    {
        if (!textInput.activeFocus && textInput.text == "")
        {

            bg.isHintIncluded = true;

            textInput.text = rootItem.editorHint;
            textInput.color = rootItem.editorHintColor;
            textInput.echoMode = TextInput.Normal;
        }

        else if (bg.isHintIncluded){

            bg.isHintIncluded = false;

            textInput.text = "";
            textInput.color = rootItem.editorColor;
            
            textInput.echoMode = rootItem.secretKey ? TextInput.Password : TextInput.Normal
        }
    }

    // --------------------------------------------------------------------------------------------------------------------------------------------------

    id: rootItem

    property color editorStartColor: "white"
    property color editorEndColor: "white"

    property string editorHint: "Input Field"
    property string editorHintColor: "gray"
    property string editorColor: "black"

    property real editorWidth: 600
    property real editorHeight: 50
    property real editorRadius: 10

    property real editorFontScale: 1.0
    
    property bool secretKey: false;
    property string secretKeyPlaceholder: "⚫"

    property alias background: bg
    property alias editor: textInput
    property alias checkbox: checkbox
    
    // --------------------------------------------------------------------------------------------------------------------------------------------------

    width: AppScreen.setScale(editorWidth); height: AppScreen.setScale(editorHeight)

    RowLayout {

        spacing: 1

        // --------------------------------------------------------------------------------------------------------------------------------------------------

        CheckBox {
            
            property real deltaX: 0

            property real pWidth: AppScreen.setScale(0.15 * rootItem.editorWidth)
            property real pHeight: AppScreen.setScale(0.5 * rootItem.editorHeight)
            property real pRadius: AppScreen.setScale(5)

            id: checkbox; tristate: false; visible: false; 
            
            Binding { target: checkbox.indicator; property: "radius"; value:  checkbox.pRadius}
            Binding { target: checkbox.indicator; property: "implicitWidth"; value:  checkbox.pWidth}
            Binding { target: checkbox.indicator; property: "implicitHeight"; value:  checkbox.pHeight}
            
            nextCheckState: function() {
                if (checkState === Qt.Checked)
                    return Qt.Unchecked
                else
                    return Qt.Checked
            }

            onVisibleChanged: {

                if(visible) {
                    
                    deltaX = pWidth + AppScreen.setScale(15);
                    bg.x += deltaX
                }

                else {

                    bg.x -= deltaX;
                    deltaX = 0;
                }
            }
        }

        // --------------------------------------------------------------------------------------------------------------------------------------------------

        Rectangle {
            
            property bool isHintIncluded: true

            id: bg

            width: rootItem.width; height: rootItem.height

            gradient: Gradient {

                GradientStop {position: 0.0; color: rootItem.editorStartColor}
                GradientStop {position: 1.0; color: rootItem.editorEndColor}
            }

            border.width: 1
            border.color: "gray"

            radius: AppScreen.setScale(rootItem.editorRadius)
            
            clip: true

            // ==============================================================================================================================================

            TextInput {
                
                verticalAlignment: TextInput.AlignVCenter
                anchors.fill: parent
                
                id: textInput

                anchors.leftMargin: AppScreen.setScale(10)
                
                font.pixelSize: ((0.095 * rootItem.width + 0.095 * rootItem.height) / 2) * AppScreen.setFontScale(rootItem.editorFontScale)

                color: rootItem.editorHintColor
                text: rootItem.editorHint
                
                focus: false

                echoMode: TextInput.Normal
                passwordCharacter: rootItem.secretKeyPlaceholder

                
                MouseArea {

                    anchors.fill: parent
                    id: indicator
                    
                    onClicked: {

                        textInput.forceActiveFocus();
                        checkAndUpdate();
                    }
                }

                onEditingFinished: {

                    checkAndUpdate();
                }
            }
        }

        // --------------------------------------------------------------------------------------------------------------------------------------------------
    }
}
