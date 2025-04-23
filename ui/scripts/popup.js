function showFeatureNotAvailableMsg(parent, scale=1.0, msg=null)
{
    
    if (msg === null) {
    
        msg = "This feature is not yet available";
    }

    var component = Qt.createComponent("../qml/widgets/PopupMessage.qml");
    var object = component.createObject(parent);

    object.msgWidth *= scale;
    object.msgHeight *= scale;
    object.msgText = msg;
}
