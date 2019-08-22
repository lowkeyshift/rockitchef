/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, { Component } from "react";
import { Platform, StyleSheet, Text, View } from "react-native";
import Router from "./src/Router";
import axios from "axios";

import { Provider } from "react-redux";
import { createStore } from "redux";
import rootReducer from "./src/components/redux/reducers";

const store = createStore(rootReducer);

const instructions = Platform.select({
  ios: "Press Cmd+R to reload,\n" + "Cmd+D or shake for dev menu",
  android:
    "Double tap R on your keyboard to reload,\n" +
    "Shake or press menu button for dev menu"
});

type Props = {};
export default class App extends Component<Props> {
  componentWillMount() {
    axios.defaults.baseURL = "http://localhost:8000/api/v1/";
    axios.defaults.timeout = 1500;
  }

  render() {
    return (
      <Provider store={store}>
        <Router />
      </Provider>
    );
  }
}
