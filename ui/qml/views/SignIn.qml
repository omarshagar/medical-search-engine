import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.9

import "../../scripts/screen.js" as AppScreen

import "../widgets" as Components

Item {
    
    property string indicator: "signInPage"

    property real pageScale: 1.0
    
    // ==============================================================================================================================

    signal joinAsGuest();

    // ==============================================================================================================================

    id: signIn

    Rectangle {
        
        anchors.centerIn: parent

        id: bg; width: AppScreen.setScale(1200); height: AppScreen.setScale(1200); radius: AppScreen.setScale(50)

        gradient: Gradient {

            GradientStop {position: 0.0; color: "#0C1E7F"}
            GradientStop {position: 1.0; color: "#612897"}
        }
            
        // 1st row
        Components.ButtonCard {

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top

            id: label; btnText: "Sign In"; btnWidth: 600 * signIn.pageScale; btnHeight: 300 * signIn.pageScale; btnRadius: 10;
            btnFontScale: 4.0; btnStartColor: "transparent"; btnEndColor: "transparent"; bg.border.color: "transparent"
            label.font.bold: true; btnIconUrl: ref_icon.user; btnIconY: 250; enabled: false
        }

        // 2nd row
        Components.TextEditor {

            anchors.horizontalCenter: parent.horizontalCenter

            id: username; editorHint: "Username"; editorWidth: 600 * signIn.pageScale; editorHeight: 80 * signIn.pageScale; editorRadius: 10;

            y: label.y + AppScreen.setScale(550);

            // ### this feature is not yet available
            enabled: false
        }

        // 3rd row
        Components.TextEditor {

            anchors.horizontalCenter: parent.horizontalCenter

            id: password; editorHint: "Password"; editorWidth: 600 * signIn.pageScale; editorHeight: 80 * signIn.pageScale; editorRadius: 10; secretKey: true
            
            y: username.y + username.height + AppScreen.setScale(15);

            // ### this feature is not yet available
            enabled: false
        }

        // 4th row
        Components.TextEditor {
            
            id: keepMeLoggedOn; editorHint: "Keep me logged on"; editorWidth: 300 * signIn.pageScale; editorHeight: 80 * signIn.pageScale; editorRadius: 10;
            editorFontScale: 2.0; editorStartColor: "transparent"; editorEndColor: "transparent"; editorHintColor: "white"; background.border.color: "transparent"
            checkbox.visible: true; editor.enabled: false;

            x: password.x - AppScreen.setScale(10)
            y: password.y + password.height + AppScreen.setScale(15);

            // ### this feature is not yet available
            enabled: false
        }

        Components.TextButton {
            
            id: forgotPassword; btnText: "Forgot Password?"; btnWidth: 300 * signIn.pageScale; btnHeight: 80 * signIn.pageScale; btnRadius: 10;
            btnFontScale: 2.0; btnStartColor: "transparent"; btnEndColor: "transparent"; bg.border.color: "transparent"
            label.font.underline: true; btn.hoverEnabled: false; rippleEnabled: false

            x: keepMeLoggedOn.x + keepMeLoggedOn.width + AppScreen.setScale(60)
            y: password.y + password.height + AppScreen.setScale(15);

            // ### this feature is not yet available
            enabled: false
        }
        

        // 5th row
        Components.ButtonCard {

            anchors.horizontalCenter: parent.horizontalCenter

            id: signInButton; btnText: "Sign In"; btnWidth: 600 * signIn.pageScale; btnHeight: 80 * signIn.pageScale; btnRadius: 10;
            btnFontScale: 1.5; btnStartColor: "#7900FF"; btnEndColor: "#7900FF"; bg.border.color: "transparent"
            label.font.bold: true;

            y: keepMeLoggedOn.y + keepMeLoggedOn.height + AppScreen.setScale(15);

            // ### this feature is not yet available
            enabled: false
        }

        // 6th row
        Components.ButtonCard {

            anchors.horizontalCenter: parent.horizontalCenter

            id: joinAsGuestButton; btnText: "Join as a Guest"; btnWidth: 600 * signIn.pageScale; btnHeight: 80 * signIn.pageScale; btnRadius: 10;
            btnFontScale: 1.5; btnStartColor: "#7900FF"; btnEndColor: "#7900FF"; bg.border.color: "transparent"
            label.font.bold: true;
    
            y: signInButton.y + signInButton.height + AppScreen.setScale(15);

            btn.onClicked: {

                signIn.joinAsGuest();
            }
        }

        // 7th row [Separator]
        Rectangle { 

            anchors.horizontalCenter: parent.horizontalCenter
            
            id: separator; width: AppScreen.setScale(450 * signIn.pageScale); height: AppScreen.setScale(1); radius: AppScreen.setScale(5)
            color: "white"
            
            x: joinAsGuestButton.x + Math.max(0, (signInButton.width - width) / 2)
            y: joinAsGuestButton.y + joinAsGuestButton.height + AppScreen.setScale(20);
        }

        // 8th row
        Components.TextEditor {

            id: msg; editorHint: "Do not have an account, "; editorWidth: 300 * signIn.pageScale; editorHeight: 80 * signIn.pageScale; editorRadius: 10;
            editorFontScale: 2.0; editorStartColor: "transparent"; editorEndColor: "transparent"; editorHintColor: "gray"; background.border.color: "transparent"
            editor.enabled: false;

            x: password.x
            y: separator.y + separator.height + AppScreen.setScale(15);
        }

        Components.TextButton {
            
            id: signUp; btnText: "Sign Up Here!"; btnWidth: 300 * signIn.pageScale; btnHeight: 80 * signIn.pageScale; btnRadius: 10;
            btnFontScale: 2.0; btnStartColor: "transparent"; btnEndColor: "transparent"; bg.border.color: "transparent"
            label.font.underline: true; btn.hoverEnabled: false; rippleEnabled: false

            x: password.x + AppScreen.setScale(180)
            y: separator.y + separator.height + AppScreen.setScale(15);

            // ### this feature is not yet available
            enabled: false
        }
    }
}