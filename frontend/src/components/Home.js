import React, { Component } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import { Actions } from 'react-native-router-flux';
import axios from 'axios';
import List from './List';

class Home extends Component {

  handleRequest() {
    // This request will only succeed if the Authorization header
    // contains the API token
    axios
      .get('/auth/logout/')
      .then(response => {
        delete axios.defaults.headers.common.Authorization
        Actions.auth()
      })
      .catch(error =>  console.log(error));
  }

  render() {
    const { buttonContainerStyle} = styles;
    return (
      <View style={buttonContainerStyle}>
        <Button title="Logout" onPress={this.handleRequest.bind(this)}/>

        <List />
      </View>
    );
  }
}


const styles = StyleSheet.create({
  buttonContainerStyle: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    backgroundColor: 'white'
}
});

export default Home;