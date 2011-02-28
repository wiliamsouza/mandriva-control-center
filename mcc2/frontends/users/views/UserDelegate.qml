//import Qt 4.7
import QtQuick 1.0

// ** Not used variable scope problem **

Item {
    //id: userDelegate
    height: 45
    width: listView.width
    Column {
        anchors.verticalCenter: parent.verticalCenter
        children: [
            Text {
                //id: userName
                text: username
                color: "black"
                opacity: 0.6
                font.bold: true
            },
            Text {
                //id: fullName
                text: fullname
                color: "grey"
            }
        ]
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            console.log("Clicked")
            listView.currentIndex = index
            //rightLoader.sourceComponent = usersForm
            fullName.text = fullname
        }
    }
}
