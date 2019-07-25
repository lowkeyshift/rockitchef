export const rootReducer = (
  state = {
    token: {},
    loading: true,
    error: null,
    recommendations: [],
    inventory_items: ["apples"]
  },
  action
) => {
  switch (action.type) {
    case "GET_TOKEN":
      return { ...state, token: action.token };
    case "SAVE_TOKEN":
      return { ...state, token: action.token };
    case "REMOVE_TOKEN":
      return { ...state, token: action.token };
    case "LOADING":
      return { ...state, loading: action.isLoading };
    case "ERROR":
      return { ...state, error: action.error };

    case "ADD_INVENTORY_ITEM":
      return {
        ...state,
        inventory_items: [...state.inventory_items, action.itemName]
      };

    case "ADD_RECOMMENDATIONS":
      return {
        ...state,
        recommendations: action.recommendations
      };

    default:
      return state;
  }
};
