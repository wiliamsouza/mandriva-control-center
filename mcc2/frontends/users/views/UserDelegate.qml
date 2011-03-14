import Qt 4.7
//import QtQuick 1.0

// ** Not used variable scope problem **

Item {
    height: 45
    width: listView.width
    Column {
        anchors.verticalCenter: parent.verticalCenter
        children: [
            Text {
                //id: userName
                text: model.user.username
                color: "black"
                //color: userDelegate.ListView.isCurrentItem ? "white" : "black"
                //opacity: 0.6
                font.bold: true
            },
            Text {
                //id: fullName
                text: model.user.fullname
                //color: userDelegate.ListView.isCurrentItem ? "white" : "black"
                color: "grey"
            }
        ]
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            console.log("Clicked")
            listView.currentIndex = index
            fullName.text = model.user.fullname
            userName.text = model.user.username
            loginShell.text = model.user.login_shell
            homeDirectory.text = model.user.home_directory

            // keep this two line at end
            groupForm.visible = false
            userForm.visible = true
        }
    }
}
