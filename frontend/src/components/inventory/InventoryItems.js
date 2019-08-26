import React from "react";
import { StyleSheet, FlatList, View } from "react-native";
import { connect } from "react-redux";
import { Card, ListItem } from "react-native-material-ui";
import { Icon } from "react-native-elements";
import { DELETE_INVENTORY_ITEM } from "../redux/actions";

const styles = StyleSheet.create({
  buttonText: {
    color: "red",
    textAlign: "center"
  }
});

const InventoryItems = ({ inventory_items, onDeleteInventoryItem }) => {
  const itemRenderer = ({ item }) => (
    <Card>
      <ListItem
        divider
        centerElement={{
          primaryText: `${item}`
        }}
        // onPress={this.clickItem.bind(this, item.recipe_url)}
        rightElement={
          <Icon
            onPress={() => {
              onDeleteInventoryItem(item);
            }}
            name="delete"
          />
        }
        // rightElement = {this.generateRightListElement.bind(this, item)}
      />
    </Card>
  );

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

const mapDispatchToProps = dispatch => {
  return {
    onDeleteInventoryItem: itemName => {
      dispatch(DELETE_INVENTORY_ITEM(itemName));
    }
  };
};

const Inventory = connect(
  mapStateToProps,
  mapDispatchToProps
)(InventoryItems);

export default Inventory;
