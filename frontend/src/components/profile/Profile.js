import React, { Component } from "react";
import { StyleSheet, Text, View } from "react-native";
import axios from "axios";
import { Button } from "react-native-material-ui";

class Profile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null
    };
  }

  componentDidMount() {
    axios.get(`recipes/users/2/`).then(resp => {
      // TODO, add this to redux
      this.setState({
        user: resp.data
      });
    });
    // fetch('http://rockitchef.com/api/v1/recipes/users/1')
    // .then( data => {
    //     return data.json();
    //   })
    // .then( data => {
    //     console.log(data)
    //     this.setState({
    //         user:data
    //     })
    // });
  }

  handleRequest() {
    // This request will only succeed if the Authorization header
    // contains the API token
    axios
      .get("/auth/logout/")
      .then(response => {
        delete axios.defaults.headers.common.Authorization;
        Actions.auth();
      })
      .catch(error => console.log(error));
  }

  render() {
    const user = this.state.user;
    return user ? (
      <View style={styles.MainContainer}>
        <Button primary text="Logout" onPress={this.handleRequest.bind(this)} />
        <Text>First Name: {user.first_name || `N/A`}</Text>
        <Text>Last Name: {user.last_name || `N/A`}</Text>
        <Text>Email : {user.email}</Text>
        <Text>Bio: {user.bio || `N/A`}</Text>
        <Text>City: {user.city || `N/A`}</Text>
        <Text>State: {user.state || `N/A`}</Text>
        <Text>Country: {user.country || `N/A`}</Text>
        <Text>
          Weight Watching : {user.weight_watching ? `true` : `false`}{" "}
        </Text>
        <Text>Vegan: {user.vegan ? `true` : `false`}</Text>
        <Text>Vegetarian: {user.vegetarian ? `true` : `false`}</Text>
      </View>
    ) : (
      <Text>Getting Users</Text>
    );
  }
}

const styles = StyleSheet.create({
  MainContainer: {
    justifyContent: "center",
    alignItems: "center",
    flex: 1,
    margin: 2
  },

  ingredient: {
    padding: 10,
    fontSize: 18,
    height: 44
  },

  textInputStyle: {
    textAlign: "center",
    height: 40,
    width: "90%",
    borderWidth: 1,
    borderColor: "#4CAF50",
    borderRadius: 7,
    marginTop: 12
  },

  button: {
    width: "90%",
    height: 40,
    padding: 10,
    backgroundColor: "#4CAF50",
    borderRadius: 8,
    marginTop: 10
  },

  buttonText: {
    color: "#fff",
    textAlign: "center"
  }
});

export default Profile;
