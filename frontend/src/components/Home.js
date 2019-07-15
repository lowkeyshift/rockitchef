import React, { Component } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import { Actions } from 'react-native-router-flux';
import axios from 'axios';
import List from './List';
import Recommendations from './Recommendations';
class Home extends Component {
  constructor(props) {

    super(props);
    this.state = {
      page:'home'
    }

  }

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
  setHomePage() {
    this.setState({
      page:'home'
    })
  }
  setRecommendationPage() {
    this.setState({
      page:'recommendation'
    })
  }
  showPage() {
    if (this.state.page == 'home'){
      return (
        <List />
      )
    } else {
      return (
        <Recommendations />
      )
    }
  }
  render() {
    const { buttonContainerStyle} = styles;
    return (
      <View style={buttonContainerStyle}>
        <Button title="Inventory" onPress={this.setHomePage.bind(this)}/>
        <Button title="Recommendations" onPress={this.setRecommendationPage.bind(this)}/>
        <Button title="Logout" onPress={this.handleRequest.bind(this)}/>
        {this.showPage()}
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
