from enum import Enum, unique

@unique
class AppGUITopics(Enum):
	SHOW_PROEJCT_VIEW_GUI = 'show_ProjectViewGUI'

@unique
class ProjectViewTopics(Enum):
	GUI_NEW_PROJECT = 'GUI_New_Project'
	MODEL_NEW_PROJECT = 'MODEL_New_Project'
	GUI_NEW_PRDUCT = 'GUI_New_Product'
	MODEL_NEW_PRODUCT = 'MODEL_New_Product'
	GUI_DUPLICATE_TUNNING_PAHSE = 'GUI_Duplicate_Tuning_PHASE'
	GUI_TREE_ITEM_RENAME = 'GUI_Tree_Item_Rename'
	GUI_TREE_ITEM_SELECTED = 'GUI_Tree_Item_Selected'
	GUI_SHOW_TOPOLOGY = 'GUI_Show_Topology'
	MODEL_SHOW_TOPOLOGY = 'MODEL_Show_Topology'
	MODEL_REFRESH_TREE_CONTRL = 'MODEL_Resfresh_Tree_Contrl'
	GUI_DUPLICATE_PRODUCT = 'GUI_Duplicate_Product'	

@unique
class TopoloyViewTopics(Enum):
	GUI_EDIT_TOPOLOGY = 'GUI_Edit_Topology'	