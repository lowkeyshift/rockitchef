const DEFAULT_STATE = {
  inventory_items: ["appless"]
};

export const InventoryReducer = (state = DEFAULT_STATE, action) => {
  switch (action.type) {
    case "ADD_INVENTORY_ITEM":
      return {
        ...state,
        inventory_items: [...state.inventory_items, action.itemName]
      };
    case "DELETE_INVENTORY_ITEM":
      return {
        ...state,
        inventory_items: state.inventory_items.filter(
          item => item != action.itemName
          // item => item.name != "appless"
        )
      };
    default:
      return state;
  }
};
