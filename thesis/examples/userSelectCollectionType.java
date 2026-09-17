public static Class<?> userSelectCollectionType(UserInteractor uI) {
  String selectTypeMsg = "Select a Collection type for the association end";
  Functions.Function1<Class<?>, String> _function = (it) -> it.getName();
  int selectedType = (Integer) 
    ((MultipleChoiceSelectionInteractionBuilder.OptionalSteps) uI
    .getSingleSelectionDialogBuilder()
    .message("Select a Collection type for the association end")
    .choices(ListExtensions.map(supportedCollectionTypes, _function))
    .windowModality(WindowModality.MODAL))
    .startInteraction();
  return (Class) supportedCollectionTypes.get(selectedType);
}