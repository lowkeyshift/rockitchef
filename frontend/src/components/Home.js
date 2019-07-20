import React, { Component } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import { Actions } from 'react-native-router-flux';
import axios from 'axios';
import List from './List';
import Recommendations from './Recommendations';
import Profile from './Profile';


import { BottomNavigation } from 'react-native-material-ui';


class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      page:'home'
    }
  }


  showPage() {
    switch(this.state.page) {
      case 'home':
        return (
          <List />
        );
      case 'recommendation':
        return (
          <Recommendations />
        );
      case 'profile':
        return (
          <Profile />
        );
      default:
        return (
          <Text> Hello</Text>
        )
    }
  }
  render() {
    const { buttonContainerStyle} = styles;
    return (
      <View style={buttonContainerStyle}>
        {this.showPage()}
        <BottomNavigation active={this.state.active} hidden={false} >
          <BottomNavigation.Action
              key="home"
              icon="hearing"
              label="home"
              onPress={() => this.setState({ page: 'home' })}
          />
          <BottomNavigation.Action
              key="recommendation"
              icon="accessible"
              label="recommendation"
              onPress={() => this.setState({ page: 'recommendation' })}
          />
          <BottomNavigation.Action
              key="profile"
              icon="group"
              label="profile"
              onPress={() => this.setState({ page: 'profile' })}
          />
      </BottomNavigation>
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
