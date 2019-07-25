export const InventoryReducer = (
  state = {
    inventory_items: ["appless"]
  },
  action
) => {
  switch (action.type) {
    case "ADD_INVENTORY_ITEM":
      return {
        ...state,
        inventory_items: [...state.inventory_items, action.itemName]
      };

    default:
      return state;
  }
};
