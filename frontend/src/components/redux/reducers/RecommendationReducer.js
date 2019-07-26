export const RecommendationReducer = (
  state = {
    recommendations: []
  },
  action
) => {
  switch (action.type) {
    case "ADD_RECOMMENDATIONS":
      return {
        ...state,
        recommendations: action.recommendations
      };

    default:
      return state;
  }
};
