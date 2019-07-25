import React from "react";
import {
  StyleSheet,
  FlatList,
  Text,
  View,
  Alert,
  TouchableOpacity,
  TextInput
} from "react-native";
import { connect } from "react-redux";
import { Card, ListItem } from "react-native-material-ui";
import { Icon } from "react-native-elements";

const itemRenderer = ({ item }) => (
  <Card>
    <ListItem
      divider
      centerElement={{
        primaryText: `${item}`
      }}
      // onPress={this.clickItem.bind(this, item.recipe_url)}
      rightElement={<Icon name="rowing" />}
      // rightElement = {this.generateRightListElement.bind(this, item)}
    />
  </Card>
);

const styles = StyleSheet.create({
  buttonText: {
    color: "red",
    textAlign: "center"
  }
});

const InventoryItems = ({ inventory_items }) => {
  const FlatListItemSeparator = () => {
    return (
      <View
        style={{
          height: 1,
          width: "100%",
          backgroundColor: "#607D8B"
        }}
      />
    );
  };

  const GetItem = item => {
    Alert.alert(item);
  };

  return (
    <FlatList
      data={inventory_items}
      width="100%"
      extraData={inventory_items}
      keyExtractor={(item, index) => `list-${index}`}
      ItemSeparatorComponent={FlatListItemSeparator}
      renderItem={itemRenderer}
    />
  );
};

const mapStateToProps = state => {
  return {
    inventory_items: state.InventoryReducer.inventory_items
  };
};

const Inventory = connect(
  mapStateToProps,
  null
)(InventoryItems);

export default Inventory;
