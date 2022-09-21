#import gui2 as gui
import plotGraphs2 as plot

class CalcInterface():
    def do1(self, plotView):
        ##def do_plot_customs_items_requiring_each_regulation_for_declarations(calculate_from_excel_file=True, use_percents=True):
        d1 = plot.howManyCustomsItemsNeedEachRegulation2({'declarations': False, 'agents': False, 'importers': False})
        d2 = plot.howManyCustomsItemsNeedEachRegulation2({'declarations': True, 'agents': False, 'importers': False})
        legend_str_without, legend_str_with = ("כולל ללא הצהרות יבוא", "רק עם הצהרות יבוא")
        self.draw_some_plot(plotView, d1, d2, legend_str_without, legend_str_with)


    def draw_some_plot(self, plotView, d1, d2, legend_str_without, legend_str_with):
        #d1, d2 = get_hardcoded_values()
        plotView.axes = plotView.figure.add_subplot(1, 1, 1)
        #pl = plt.bar(d1.keys(), d1.values(), width=0.5, linewidth=2, label=legend_str_without[::-1])
        plotView.axes.bar(d1.keys(), d1.values(), label=legend_str_without[::-1])
        plotView.axes.bar(d2.keys(), d2.values(), label=legend_str_with[::-1])
        plotView.axes.set_title("כמה פריטי מכס צריכים אישור זה"[::-1], fontsize=15)
        plotView.axes.set_xlabel('קוד אישור'[::-1], fontsize=15)
        plotView.axes.set_ylabel('מספר פריטים'[::-1], fontsize=15)
        # self.axes.set_visible(False) This remove the graph from view
        plotView.axes.set_xticklabels(d1.keys(), rotation=90)
        plotView.axes.legend()


def plot_these_data(d1, d2, legend_str_without, legend_str_with, use_percents = True):
    plt.figure(figsize=[20, 7])
    pl = plt.bar(d1.keys(), d1.values(), width=0.5, linewidth=2, label=legend_str_without[::-1])
    index = 0
    for bar in pl:
        x_code = list(d1.keys())[index]
        description_value = bar.get_height()  # if we want description of each bar to be total number of such items
        if use_percents:
            percent = 100 * d2[x_code] / d1[x_code]
            description_value = str(int(percent)) + "%"  # if we want description of each bar to be percent of count without 0 number of declarations from count with any number
        plt.annotate(description_value, xy=(bar.get_x() - 0.07, bar.get_height() + 10), fontsize=8)
        index = index + 1

    pl2 = plt.bar(d2.keys(), d2.values(), width=0.7, label=legend_str_with[::-1])
    plt.title("כמה פריטי מכס צריכים אישור זה"[::-1], fontsize=15)
    plt.xlabel('קוד אישור'[::-1], fontsize=15)
    plt.ylabel('מספר פריטים'[::-1], fontsize=15)
    plt.xticks(fontsize=10, rotation=90)
    plt.legend()
    plt.show()





if __name__ == "__main__":
    import gui2 as gui
    calcInterface = CalcInterface()
    myApp = gui.MyApplication(calcInterface)
    #draw_some_plot(myApp.plotView,  "כולל ללא הצהרות יבוא", "רק עם הצהרות יבוא" )
    #do1(myApp.plotView)
    myApp.mainloop()
