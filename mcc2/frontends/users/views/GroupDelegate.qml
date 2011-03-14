import Qt 4.7
//import QtQuick 1.0

// ** Not used variable scope problem **

Component {
    //id: groupDelegate
    Item {
        height: 45
        width: listView.width
        Column {
            anchors.verticalCenter: parent.verticalCenter
            children: [
                Text {
                    //id: groupName
                    text: groupname
                    color: "black"
                    opacity: 0.6
                    font.bold: true
                }
            ]
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                console.log("Clicked")
                listView.currentIndex = index
                //rightLoader.sourceComponent = groupsForm
                groupName = groupname
                userForm.visible = false
                groupForm.visible = true
            }
        }
    }
}
