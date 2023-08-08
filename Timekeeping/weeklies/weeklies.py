from tabulate import tabulate
import sys

class Weekly:

    def __init__(self, s_file, debug, f_contents=None):
        self.source_file    = s_file
        self.billing_units  = None
        self.docs           = f_contents
        self.time_summary   = None
        self.debug          = debug


    def _pdebug(self, p_val):
        if self.debug == True:
            print(f"[DEBUG] {p_val}")


    def get_billing_units(self):
        """Group things by billing units"""

        bu_list = []
        tickets = []
        for day in self.docs:
            self._pdebug(f"Day: {day}")
            # get a billing unit 
            for unit in day['billing-units']:
                self._pdebug(f"Checking {bu_list} for {unit['number']}")
                if unit['number'] not in bu_list:
                    # if we haven't seen this billing-unit # before, let's get all of the tickets associated with it
                    bu_list.append(unit['number'])
                    self._pdebug(f"Unit        : {unit}")
                    print(f"Billing unit: {unit['number']}")
                    # loop through the entire doc, look for this BU and its features
                    for f_day in self.docs:
                        for f_unit in f_day['billing-units']:
                            self._pdebug(f"Unit           : {f_unit}")
                            if unit['number'] == f_unit['number']:
                                # 
                                for f_item in f_unit['features']:
                                    if not f_item['ticket'] in tickets:
                                        try:
                                            print(f"Ticket #       : {f_item['ticket']}")
                                            print(f"Description    : {f_item['description']}")
                                            tickets.append(f_item['ticket'])
                                        except KeyError as ke:
                                            self._pdebug(f"Key Error: {str(ke)}")
                                            print("Ticket #       : [no ticket]")
                                        # find other ticket numbers under this billing unit and collate the tasks
                                        # for each day, each billing unit, and each feature, get same info
                                        for g_day in self.docs:
                                            self._pdebug(f"Inner loop g_day: {g_day}")
                                            for g_unit in g_day['billing-units']:
                                                for feature in g_unit['features']:
                                                    if feature['ticket'] == f_item['ticket']:
                                                        try:
                                                            print(feature['tasks'])
                                                        except KeyError as ke:
                                                            self._pdebug(f"Key Error in get_billing_units: {str(ke)}")
                            else:
                                self._pdebug(f"Skipping unit {f_unit['number']}")
                print()
        self._pdebug(f"billing units: {bu_list}")
        self._pdebug(f"tickets      : {tickets}")
        self.billing_units = bu_list


    def get_time_summary(self):
        """Get summary of billing units and hours for each"""

        time_summary = {}
        for day in self.docs:
            self._pdebug(f"Day: {day}")
            for item in day:
                # day, date, billing-units
                if item == "billing-units":
                    for unit in day[item]:
                        self._pdebug(f"Unit: {unit}")
                        self._pdebug(f"Billing unit: {unit['number']}")
                        if not unit["number"] in time_summary:
                            self._pdebug(f"Adding new billing unit: {unit['number']}")
                            time_summary[unit["number"]] = unit['hours']
                            #self._pdebug(f"Hours: {day[item][0]['hours']}")
                            self._pdebug(f"Hours: {unit['hours']}")
                        else:
                            # assume hours exist, add to existing
                            cur_hours = time_summary[unit['number']]
                            new_hours = unit['hours']
                            new_total = cur_hours + new_hours
                            time_summary[unit['number']] = new_total
                            self._pdebug(f"Hours: {time_summary[unit['number']]}")
        self._pdebug(f"time_summary: {time_summary}")
        self.time_summary = time_summary
        return True


    def get_days(self):
        """Get Days of the Week that are present in the report"""

        for day in self.docs:
            self._pdebug(f"Day: {day}")
            print("-------------------- ")
            print(f"Day  : {day['day']}")
            print(f"Date : {day['date']}")
            print()
            for b_unit in day['billing-units']:
                print(f"Unit : {b_unit['number']} ({b_unit['title']})")
                print(f"Hours: {b_unit['hours']}")
                print("Features:")
                for feature in b_unit['features']:
                    try:
                        print(f"      {feature['ticket']}", end="")
                    except KeyError:
                        print(f"      [no ticket #]", end="")
                    try:
                        print(f" {feature['description']}")
                    except KeyError:
                        print(f"      [no description]")
                    print()
                    try:
                        print("         ", feature['tasks'].replace('\n', '\n          '))
                    except (KeyError, AttributeError):
                        print(f"          [no tasks]")
                        print()
        return True


    def data_tabulator(self, tabulated_unit):
        if tabulated_unit == "weekly_totals":
            headers = []
            hours = []
            for unit in self.time_summary:
                headers.append(unit)
            for unit_hours in self.time_summary:
                hours.append(self.time_summary[unit_hours])
            self._pdebug(f"headers: {headers}; hours: {hours}")
            print(tabulate([hours], headers=headers))
            print()
        return True


    def data_parser(self):
        self._pdebug(f"Full document: {self.docs}\n\n")
        # Summarize hours by billing unit(s)
        print(f"Building time summary")
        self.get_time_summary()
        self.data_tabulator("weekly_totals")
        # Break things out according to Days of the Week
        print("Summarizing by Days of the Week")
        self.get_days()
        # Group all billing unit(s) into work summary
        self.get_billing_units()
        return