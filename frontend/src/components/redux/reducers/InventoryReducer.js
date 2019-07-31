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
    case "DELETE_INVENTORY_ITEM":
      return {
        ...state,
        inventory_items: inventory_items.filter(
          item => item.name != action.itemName
        )
      };
    default:
      return state;
  }
};
