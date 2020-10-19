# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('B', '  52 ', 'ALA', 0.039323589512037425, (10.012000000000002, -22.768, 34.191)), ('B', ' 138 ', 'ASN', 0.04427813081398081, (-14.945000000000004, -26.543, 4.071)), ('D', '  86 ', 'GLU', 0.044537037058637194, (59.69499999999999, -43.878999999999984, 51.31900000000002)), ('D', ' 111 ', 'GLY', 0.024246217520265685, (67.61900000000003, -45.672, 59.127)), ('D', ' 155 ', 'ASP', 0.01812848643752296, (95.58800000000002, -55.832999999999984, 34.862)), ('L', '   2 ', 'ILE', 0.06901398292281732, (24.132000000000005, -28.288, 72.814))]
data['omega'] = [('A', ' 161 ', 'PRO', None, (-20.607, 0.141, 16.209000000000003)), ('A', ' 163 ', 'PRO', None, (-20.901, -5.882, 17.945)), ('B', '   8 ', 'PRO', None, (6.748999999999999, -23.495, 16.461)), ('B', ' 141 ', 'PRO', None, (-5.359000000000001, -28.001, 4.449)), ('C', '  33 ', 'TRP', None, (33.988, -34.698999999999984, 36.256)), ('C', ' 160 ', 'PRO', None, (63.35199999999999, -47.173999999999985, 21.521)), ('C', ' 162 ', 'PRO', None, (60.34, -49.925, 26.319)), ('D', ' 145 ', 'PRO', None, (73.21700000000001, -48.369, 51.713)), ('H', ' 154 ', 'PRO', None, (8.122999999999998, -60.28499999999998, 78.19300000000001)), ('H', ' 156 ', 'PRO', None, (7.025, -55.27899999999999, 81.481)), ('L', '   8 ', 'PRO', None, (28.015, -33.45699999999999, 90.601)), ('L', '  95 ', 'PRO', None, (13.594999999999999, -27.659999999999993, 67.61)), ('L', ' 142 ', 'PRO', None, (23.97100000000001, -50.276, 105.563))]
data['rota'] = [('B', '  34 ', 'LEU', 0.28256165186466553, (9.802999999999997, -17.992, 33.182)), ('B', ' 107 ', 'LYS', 0.2137641962411937, (-4.106, -32.041, 12.361)), ('B', ' 108 ', 'ARG', 0.19156237184031555, (-6.817, -32.93199999999999, 9.769)), ('B', ' 172 ', 'THR', 0.01341348294246853, (-11.873000000000003, -27.859999999999992, 8.674)), ('A', '  59 ', 'ASN', 0.1887589374908805, (5.6450000000000005, -0.134, 37.315)), ('A', ' 201 ', 'SER', 0.24022695659405352, (-32.454, -30.123, -5.831)), ('A', ' 203 ', 'LEU', 0.0522587928796322, (-32.874, -24.353, -4.517)), ('A', ' 224 ', 'LYS', 0.06152846959235057, (-34.480000000000004, -12.818999999999997, 1.7820000000000003)), ('D', '  70 ', 'SER', 0.10262877209507638, (51.012, -15.971999999999996, 56.849)), ('D', '  92 ', 'GLN', 0.007217720272421155, (47.71800000000001, -29.833999999999993, 44.318)), ('D', '  98 ', 'ASN', 0.18957503036931725, (43.15, -24.607, 35.927)), ('D', ' 132 ', 'ASN', 0.2973306896505727, (83.80599999999997, -57.658999999999985, 16.124)), ('D', ' 174 ', 'ASN', 0.23316168029984427, (64.22800000000001, -52.457, 49.428000000000004)), ('C', '  11 ', 'LEU', 0.02200865859542305, (57.914, -43.288, 19.712)), ('C', '  18 ', 'LEU', 0.1327041798851168, (49.353, -38.66, 18.468)), ('C', '  21 ', 'SER', 0.16939398826626467, (42.50500000000001, -42.795, 24.845000000000002)), ('C', '  30 ', 'SER', 0.09513855139686334, (28.83100000000001, -38.724, 32.92000000000001)), ('C', '  55 ', 'THR', 0.22941709750966752, (26.19899999999999, -31.45, 33.33200000000001)), ('C', '  67 ', 'LYS', 0.26570861721121364, (47.095, -24.848, 24.748)), ('C', '  90 ', 'THR', 0.05426097650498142, (60.907, -33.047, 23.166)), ('C', ' 163 ', 'VAL', 0.2627885497103041, (62.705999999999996, -54.361, 26.776)), ('L', '   9 ', 'SER', 0.08786936513364313, (27.440000000000005, -38.034, 88.622)), ('L', ' 108 ', 'LYS', 0.0034649905298587288, (23.839000000000006, -41.421, 103.81200000000001)), ('L', ' 109 ', 'ARG', 0.1798743926884185, (21.67300000000001, -43.20999999999999, 106.479)), ('H', '  76 ', 'ASN', 0.2158062234600818, (-8.242, -36.184, 74.448)), ('H', ' 112 ', 'GLN', 0.2726009922209095, (4.096000000000002, -42.975, 83.99400000000001)), ('H', ' 137 ', 'SER', 0.12477615828229072, (8.126, -64.849, 108.742)), ('H', ' 206 ', 'ASN', 0.2444968030448158, (-1.0210000000000043, -57.409, 86.01400000000001)), ('R', ' 341 ', 'VAL', 0.14878682511865596, (11.543, -13.722, 51.144)), ('R', ' 408 ', 'ARG', 0.012515093765468076, (26.037, -25.21, 60.57)), ('R', ' 518 ', 'LEU', 0.23253778955118026, (10.757, -4.039, 72.951)), ('R', ' 528 ', 'LYS', 0.11305738599581656, (-6.2040000000000015, -13.967999999999996, 66.33)), ('R', ' 529 ', 'LYS', 0.0, (-8.48, -17.11, 65.997))]
data['cbeta'] = []
data['probe'] = [(' R 339  GLY  O  ', ' R 343  ASN  HB2', -0.659, (7.941, -15.581, 47.741)), (' R 431  GLY  HA2', ' R 515  PHE  CD2', -0.449, (12.938, -15.707, 66.113)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.407, (13.251, -32.561, 91.844)), (' L  21  ILE HD12', ' L 103  THR HG21', -0.407, (24.061, -34.189, 91.847))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
