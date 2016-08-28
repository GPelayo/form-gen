from data_pipeline.common import HTMLProfile


class ResMatrixHtmlProfile(HTMLProfile):
    def __init__(self):
        super().__init__()
        self.html_pages['Itinerary'] = [('#CPH1_spResvID', 'pk'),
                                        ('#CPH1_spPnr', 'pnr'),
                                        ('#CPH1_spChannel', 'channel'),
                                        ('#CPH1_spCheckIn', 'date_in'),
                                        ('#CPH1_spCheckOut', 'date_out'),
                                        ('#CPH1_spAdultsChildren', 'Rm/Ad/Ch'),
                                        ('#CPH1_spRoomType', 'Room Type'),
                                        ('#CPH1_spRateCode', 'Rate Plan'),
                                        ('#CPH1_spBookDate', 'Book Date'),
                                        ('#CPH1_spRoomAmount', 'room_rate'),
                                        ('#CPH1_spRoomTaxes', 'room_taxes'),
                                        ('#CPH1_spRoomTotal', 'room_total'),
                                        ('#dvCalendar', 'Calendar')]

        self.html_pages['Guest Info'] = [('#CPH1_spFirstname', "first_name"),
                                         ('#CPH1_spLastname', "last_name"),
                                         ('#CPH1_spOptin', "Email Opt In"),
                                         ('#CPH1_spReturnGuest', "Returning Guest"),
                                         ('#CPH1_spAddress', "street"),
                                         ('#CPH1_spCity', "city"),
                                         ('#CPH1_spState', "state"),
                                         ('#CPH1_spCountry', "country"),
                                         ('#CPH1_spLoyaltyID', "Loyalty ID"),
                                         ('#CPH1_spEmail', "Email"),
                                         ('#CPH1_spPhone', "phone_number"),
                                         ('#CPH1_spCompany', "Company"),
                                         ('#CPH1_spSGA', 'sub_channel'),
                                         ('#CPH1_spBillAddress', "Billing Address"),
                                         ('#CPH1_spBillCity', "Billing City"),
                                         ('#CPH1_spBillState', "Billing State"),
                                         ('#CPH1_spBillZip', "zip_code")]

        self.html_pages['Comments'] = [('#CPH1_spGstComment', "Guest Comment")]

        self.html_pages['Billing / Policies'] = [('#CPH1_spGuarMethod', "Guest Method"),
                          ('#CPH1_spCardHolder', "Credit Card Holder"),
                          ('#CPH1_spCardType', "Credit Card Type"),
                          ('#CPH1_spCardNumber', "Credit Card#"),
                          ('#CPH1_spCardExpire', "Expiration Date"),
                          ('#CPH1_spIata', "IATA"),
                          ('#CPH1_spCompanyName', "Travel Agent Company"),
                          ('#CPH1_spTaPhone', "Travel Agent Phone#"),
                          ('#CPH1_spTaAddress', "Travel Agent Address"),
                          ('#CPH1_spTaCity', "Travel Agent City"),
                          ('#CPH1_spTaState', "Travel Agent State"),
                          ('#CPH1_spTaCountry', "Travel Agent Country"),
                          ('#CPH1_dvCancellation', "Cancellation Policies")]

        self.html_pages['Guarantee'] = [('#CPH1_dvGuarantee', "Guarantee Policies")]

        self.html_pages['Restrictions'] = [('#CPH1_dvGuarantee', "Restriction Policies")]

    # table_fields = [('dvCalendar', 'Calender')]