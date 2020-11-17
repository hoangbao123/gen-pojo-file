public class random{ 
    private Application application;

    private Borrower borrower;

    private List<Meta> meta;

    public static class Application{ 
        private String product;

        private Integer amount;

        private Integer term;

        @SerializedName("limit_slider_changed")
        @JsonProperty("limit_slider_changed")
        @Column(name = "limit_slider_changed")
        private Integer limitSliderChanged;

        @SerializedName("revenue_amount")
        @JsonProperty("revenue_amount")
        @Column(name = "revenue_amount")
        private Integer revenueAmount;

    } 

    public static class Borrower{ 
        @SerializedName("full_name")
        @JsonProperty("full_name")
        @Column(name = "full_name")
        private String fullName;

        @SerializedName("mobile_phone")
        @JsonProperty("mobile_phone")
        @Column(name = "mobile_phone")
        private String mobilePhone;

    } 

    public static class Meta{ 
        @SerializedName("utm_medium")
        @JsonProperty("utm_medium")
        @Column(name = "utm_medium")
        private String utmMedium;

        @SerializedName("utm_source")
        @JsonProperty("utm_source")
        @Column(name = "utm_source")
        private String utmSource;

        private String ga;

        private String uid;

    } 

} 

