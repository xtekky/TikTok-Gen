import requests
import json
import time
import threading
import random
import re
import curlify

from urllib.parse import *
from utils.signer.signature import Signer
from utils.bogus import XBogus
from utils.mstoken import msToken

class Gen:
    def __init__(self):
        self.__client = requests.Session()
        self.__wid = None
        
    def __base_params(self, __url_base: str, __aid: int = 1988, addon: json = {}):
        
        __base_params = {
            "aid"             : __aid,
            "app_language"    : "en",
            "app_name"        : "tiktok_web",
            "battery_info"    : 1,
            "browser_language": "en",
            "browser_name"    : "Mozilla",
            "browser_online"  : True,
            "browser_platform": "Win32",
            "browser_version" : "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "channel"         : "tiktok_web",
            "cookie_enabled"  : True,
            "device_id"       : self.__wid,
            "device_platform" : "web_pc",
            "focus_state"     : True,
            "history_len"     : "2",
            "is_fullscreen"   : False,
            "is_page_visible" : True,
            "os"              : "windows",
            "region"          : "FR",
            "screen_height"   : 1080,
            "screen_width"    : 1920,
            "tz_name"         : "Europe/Paris",
            "webcast_language": "en",
        }
        
        __base_params.update(addon)
        
        __base_params.update(
                {
                'msToken'     : '%s' % msToken.get_value(),
                "X-Bogus"     : '%s' % XBogus.get_value(),
                "_signature"  : '%s' % self.__get_signature(__url_base + urlencode(__base_params))
            }
        )

        return urlencode(__base_params)
    
    def __base_headers(self, addon: json = {}) -> json:

        __base_headers = {
            'authority'         : 'www.tiktok.com',
            'accept'            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language'   : 'en',
            'cache-control'     : 'no-cache',
            'pragma'            : 'no-cache',
            'sec-ch-ua'         : '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile'  : '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest'    : 'document',
            'sec-fetch-mode'    : 'navigate',
            'sec-fetch-site'    : 'none',
            'sec-fetch-user'    : '?1',
            'cookie'            : str(
                    self.__cookie_to_str(
                    self.__client.cookies.get_dict()
                )
            ),
            'upgrade-insecure-requests': '1',
            'user-agent'               : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        
        __base_headers.update(addon)
        
        return __base_headers
    
    def __cache_token(self, __wid: str) -> str:
        return '{%22_type_%22:%22default%22%2C%22user_unique_id%22:%22' + __wid + '%22%2C%22timestamp%22:' + str(int(time.time())) + '}'
    
    def __cookie_to_str(self, cookies: json) -> str:
        cookies_str = ""
        for i in cookies.items():
            cookies_str = cookies_str + i[0] + "=" + i[1] + "; "
        return cookies_str[: len(cookies_str) - 2]
    
    def __get_signature(self, __url: str) -> str:
        with Signer() as signer:
            verify_fp, signature, device_id, tt_params = signer._sign(__url)
            return signature

    def __get_wid(self) -> str:

        __html = self.__client.get(
            url = 'https://www.tiktok.com/signup/phone-or-email/email',
            headers = self.__base_headers()
        )
        
        return str(
            re.findall(r'wid":"(\d*)"', __html.text)[0]
        )
        
    def __account_info(self):
        __base_url = (
            'https://'
                + 'www.tiktok.com'
                + '/passport/web/account/info/?'
        )
        
        __base_params = self.__base_params(
            __base_url, 
            1459
        )
        
        __response = requests.get(
            url = (
                __base_url + __base_params
            ),
            headers = self.__base_headers()
        )
        
        return __response.json()
    
    def __compliance_settings(self):
        __base_url = (
            'https://'
                + 'www.tiktok.com'
                + '/api/compliance/settings/?'
        )
        
        __base_params = self.__base_params(
            __base_url, 
            {
                'priority_region': '',
                'referer': '',
                'fromWeb': '1',
                'from_page': '',
            }
        )

        __response = requests.get(
            url = (
                __base_url + __base_params
            ),
            headers = self.__base_headers()
        )
        
        return __response.json()
    
    def __verification_age(self):
        
        __base_url = (
            'https://'
                + 'www.tiktok.com'
                + '/api/v3/register/verification/age/?'
        )
        
        __base_params = self.__base_params(
            __base_url
        )
        
        __response = requests.post(
            url = (
                __base_url + __base_params
            ),
            headers = self.__base_headers(),
            data = {
                'fromWeb'            : '1',
                'source'             : 'web',
                'session_registered' : '1',
                'birthday'           : f'1985-03-03',
                'tt_csrf_token'      : self.__client.cookies.get_dict()['tt_csrf_token'],
            }
        )
        
        return __response.json()

    def main(self):
        self.__wid = self.__get_wid()
        self.__client.cookies.set(
            "__tea_cache_tokens_1988", self.__cache_token(self.__wid)
        )
        self.__compliance_settings = self.__compliance_settings()
        self.__account_info = self.__account_info()
        self.__verification_age = self.__verification_age()
        print(self.__verification_age)


# Gen().main() 
if __name__ == '__main__':
    # Gen().main()
    response = requests.get('https://s20.tiktokcdn.com/tiktok/common/init.js?async')
    print(response.text)
    
    __json = {
        'htc6j8njvn-a': '', #'PXeRsqKamvjIu-=-lVMXIiJ57UftENfaCp1rMicezu-qLclLOqeBCbb6IzJ1OooNaqhu8lHg7e5fL=-H-vmSCtFjKcTlWbpumxAajHc9yu2ZT7XnInOJF3D3fCgHtDpj2-DVz6cKGnhFc7wkWZ97fxNCrYUgMVqW3=s-S5d5uagqWyZT_qLMn5XrsZrOr2StLlv-1xaSbw7lsc2-zmqTOhjkDRddLbdBpO=Ct5_8Btfddjv3RqEK=KlbN2fgyngCPSi7SaHIhgitEzLgTOKGO175Xn5um1n68SwkXNLHfauF2HTsoLVk_Seiz8YYnMFjws8Fsze8Wb6kSDdijOcIOhNblrl90HbxXod5J0_jBlrZTtWKMy3rXBh_WBa=Dh8OJIT1ie553OF79sGBfRmWl1cK19aNs9jDMn_8aCVLw4jcdn8tWeVKUhCSXTmausH3caRtAL5rn6vZFCw4U4wslBDiZUjzpU8W=jmSTsDyFzyR78-ecJ8riofdo8bhW5Yxhaj98UrO8YrXSitA2eiBj2JJn=UDyMjVqujMbtoO-lAFPA=gVpEE1=o82qvan==GgMvdT7O7IKP4BJvzcVBOoFiqGa6P_ivZFCWHSIYVEMrikHpy36CxFWs4XrLlkuEdAO-d4ggM__Kv8piFw=w4fh3Fc5NYF_KqwqNCSzmSAwzUCNZBUJmL_GvFbImEKkKtoRDtH26LfAD2PsDeEc4Si05XEKDv_83PfvgBE-cf_HnVrs=q_12-LcFzt5tUVpPkPm9_uZOKkdYMv3nj_wJo=w=n9odLcGFtlr-JRhKCvnCLvbaRz8UdM-mVach5yP=uni9iYZ1=1XhY22r=pXJJ95YbJ-8w4POhxCc99_N_wZKOIJM0Bhy7n0AT1ijxBzS-qjepiXMImW4vLA=rH9Kg=ryURLIeBqwAxm2=HAs0g57r6ZP_zpgus5Nvc3DgO6786G5FtHIN=UW6GonwH5=PVI8ij7gMsPG9mVXIvB22jHwZid05UVq=fwq5BcYdAbGptecXCENY5BzKqcfD2SC=kZvM3ub2rgwu0XB-aTE_ND5_J8GU2i6n_TGxXNiInbK-ZMUNW7uUn2-buZVrAef-PS3inKOntlzAUNEWx1Kv703=7e3=AlkDzKWS02UqfRNjrKdzlOrBIUblzn7m_=slCej0KC5mELhBaCA23Kq_tjvf-yXstoBneJcIxGL40y7Nof3d=BFRLL-0B5hUrTRmNmVo2Myp1UCeT9sCZ6AjgV2fskH-lcph=uU7y5nCW74akN=RUip_J4pKCaRmqNK2RHma2=27NMu84SWYxuuoqdboZD58qJMXs52GgD_R6AvCYcjewtWuUCyxoFYTu==T-_l_vB4g3dJ_9oX0ru95hT29N07BHPwXrS05cupphbndZgUynmEIrWj-bxdnRKP=ma0bOiogDPoL-XPd0JLadiM9_eLtUGjajXF17cPVDZ5D9JEH21FexiDcTrIEz8SIyw7hv6HsPhqLY7YqxB--ZTgvHXMFof-H2iobfnDgReVqKvpoCLMzAqtVCWl2Kr3_b=Lof6U2Ton9oim593xIr1NBoRHDdKgNLHkZUvlsfatCpeB=weKV8Z6d=CS2k1lmB7bz7KiAk_Zngx6JnWMFADF1RGVXwrHPh56KcXbJZfLUMRWLRC_i2AD9Xl76WSsH8bq5K9YlJGgNM6wufA-cAttz9EP81pCxZny7TS5Gr1TIHUWiTS5NZtVblvVJbimnvpR1Rb-K2KoJgSIWf54POZ7ptoU29TKYKItpBMWw4vgtIeSj4LaiuMy6URVsebxpXWjHT4xiTqfZabckXAwFzN3Tqd7qCbDmZg2u3Gr6ArSLLA376s_EiY0fmSR6BwohXXlVgeRT8uVlMKm6=7KuYaB_28x1bCwaquH43s7ouNicdwZVS7mRJaPeOD-Vq8_9SP6RlfiUqzZkH4=YjI0V-ngxTfmA2XoHJeP3tqCEj3tfkJ4NrkX9tG1c5MOvScj0jxoScRF1C9IdPno9Fhchx-S-BkREnL7ozBoZSfx=u699wqpL_BksgJdXwzvIxw25oqqe2ECtr=uVRuIJAeSmOZx1FYq_YAL1cViOlZtxDItdj1EidTPv=SG0z5C8Y7MoM9C1VGT19wlZlZu1V5augR_PFB5zo-_osEEVTP0i6d8OEALMP0Xcah-IDhk5-o1EnJbzXfiIjnECwAXurETNRk7bGoiO5efEiBS9vXyS9LKIVLlsooFa8SmjevjKHcxs5aPE5pHL8WdMksA1KbErZ6rU_p36cRLqb0JGsGWANMLXNSc8wZm=0lvYbks=qlKO5x34xREgqjH2Rt16nfdMHiPNwbws2e3Y0YWe-VrPJJuMeL5HG202FA5pJAeZGbxiEPxgzKeRM5Jc_8m5dzGX=a=y_OWE9t4FJx=ZP1sxXvbpEewrlTZp78WKtfV5fwS005aptv_cEX_t36z6hfogDqEPu9yss3VUq0mmpyqTEzDFZ-4iZttwace17A=UysyZYaNg3S6zfd=MY0ew8ysyfzg2vKnwaDnDLFs7IP0qm92pZn5VHg2_CW-sR5HrJT8hf5i71vY1MM7-aBblrDbl0tefE=CSwXMGLHMTT4-tvubcZPLC6Wu8k1KhdMoEP99PqKW3fXpl=Ye47-qFX-dcoGkgDwWuDm3qOz0jSg_0fJ9cY1VESyeqJk9gDFS761JpSG0Hr6yeIHnc0bZbIL33MaJ1RwI2pDmN=P8e3oPkqHC=pkLpgHznRjt8nF2kp2Giicd8ZcqrY-NvOIJm=4hZgPadVYVac6lNMCSpNXsF1Bf-MfGW0xOPAR8SlckMKsx4khbAiBo6yT9ufNJSjZ1=xNa9uJNhRaxajlCzZDbhXz2FUj-1arxFGKCw5NYwSZyrjE=CuWjPxS6aKc_WpL3AqFWBp7Yp_6N6sJEo8GVDsDKbR3J7ShSwa=wTk_S9maYVvMht08_s7CRZRPCtf4LSpO5x-S=aUiv7_9RSd0ctqumfJyprjSd8OFR=MbFtm1-5MOwZ8YWgCFUsTle4LJ34MgM_NxeAvWZEpnbizzhOiXdY-7uLif_VkayGtYMWFXVXZV4WGTif4kUKc5Del_oVo1Loq_UIvbG_XNxR8=cK3onjZh_hd1bf-aCfBB5tTNDyHm0SUmR2_exC9kl_D-YUo682NjOUU2vDJ_6rZhoYjc-YZ=ha9uy-S4Yj10ZsawY3kPjyfB_dSOv10V26kdcvPctS_mlZNr5305PxKZKhF8G=LSgIfeDinywgVzexbIW=dSH2Edo=sbmpridL1ZbtsRp8jfO0IdimOu6lX-dMt7StWGoZ70MRLXYyyR9wPPFolcLC=7jNuer0F8k9ilxlqSWbc=h0aEtGEDW1l6sM-Se978NDy4ixA_tLYfmvofllnk-=X9zlitTHOrw0AWGNnXUtxIuV-q_ttVIv2pZgrXRFEK1UW1bstGK_rR08LkTC5S_4kUgIk-OKnvEYK5EUnsK8=rwWLg0AK=7xjPk5bozkCYOFrGiln9wVbGnwwjRI0BJhlH61h-Gr-J0H=BApVea0Dwf=8ye4_n5D_NSwEaAkDXDBfbDBM5mneVwotA6jRSuu8jpbgUTLK5m_DBqM2KhUhuKXGXVG=Xs6wz1fYndUuS_46x3ouYnJVeaRVk5AcjyhF3lUV4ShdzyfPfTmqc_C7aovplqcTzitqfyL91CF8JklRk-l-FhgOoSIW-lxt2zXksWH65zJLDYmqC4vFR65dXV3p5VghZo=eREosKBgt0=3ljUSgmWeSKiUFwhz0bxfLoxXx9-j4mZxVogtPoXCFLs8N=fqO2AYMxY4DiSpOUvxTP=Ef4eAC0JRHa=FjqZbUaWfpwc5jmCP=wqW2mFPN3uj65cEXKXSulhtF0a_kZ_jdwtr6lbllv5PvoLeh1Uk322A8--9kCVrNBI-ceG7UND7MXai=DU7x6GKUcqI1uO3wMcA4qDM4P=335nkFSgqTVEZI4SGXLeS1PNalGGAZkNXDNDgKKK0FZuefKUakC=I-M1lyZSi6OokEWBrJYlT8cIBnX5bCvFa=r6NG=B59zrIO-8IBHfrRfwWxiuutmLPgGhzCNby4A8CsHeMfyzHpJdn58WTApnkzahRWTd80a_bm5f5BmIy=e56E3V87rhnsqBABndlUG7WAsX8PFOA2MHSXI6--ANdHKthEcEbdCE-lMqi5azUZWZMO6o7SHkPCp5JRf0uMnthVyjmoSnVeJr8dAu8qW_itUerbSOS_mRDdB9HVxHRYypsY=ISeTcqNNt5OKhLnG=2vYe2jNq6o80d5ueCnLjb=1vNAaJA4nMJd2hFHqT86lvE5SFlYRgj1pT7VP9x7nmafrJ=K4b5k7nH9bzG-x69HHhNlSo7-gAcdX2pUUfCk60sl3b4xuYYNZLFOAlmwwcGUqTaJEbWOnR7k_K39TCdKlu=ZY3z9V48hjzO=w-k6m_4skvxc-idiiBHd-WvKSj8Fx4HzlAL_Ll1_n8tzsMz0DUwtkT62tn=HI3M882WoX7j3qD_h3jgI79IYIHisUb8kMdtT_kp4UgaTuIKmLYkE3NBcO_tjjXI_6YcORHPFzgvijVV8ZDLkvTRFr3peDLnYhUkH6W8N659MTcXJ-6ieAgAbWi7Ly2rOGCBZO9t_7_A4_smyJgYEnRBJy8XrsGgivIn_s_lmMch_gFjxRDZWLYGipsFnbvNc0LMlWf1yGjfi67iOjm0UDJt7crHWZa0X5BcAkLi28hsP2g5-PW-8SvO_WMAodGUEN8yvPd-EccyF6KIPuEebgA6bnE5TgX=yD6OirFuCJVXWV6SlH277YpS1M6lF7qM2fU9oeulUPmW2GMINrskq2Z31p1bn22lqGelW7bwRHnG7w1N04vA3rTYFZ1_RRjM17gt1Xw5AvJTNgvste1cR8wUlUZchUj0by3zPIf9gCiCx7W27rAI0UnvWT8cZ7I7MqWBXc-rso4lAlaacmxA8etd-x5tC5LDdPPya49cM1=iXpB2xWImipqS6_VDW5l3M62ETMdpO=VHsB_XoHHRWa1lZ8Of9U5468h0udSds1EFZcpFmKNEh3jcX0upMMyYUfyWhP5lvJl7w7twzOcFaH38p5JBpahj2v5H9gTPuBShEtkO6cV0e9evVKhaJjOlbYD8inAdulOLOGCcF1ssHhHhrOg423pmZ5=rpECF2lFUgP26kts-GvsZDVIB5dN5hcPk2_h3=jP3LVpcF-tV6f0DfBa4HZxrSWU=cwyVK6ixacKZ3Ir7Gk3GiarPfg=aXDGuwOzVTgGNe7C=1O4A4xoJBzvcqI-MonaVjC_F34DknhdzBkH4DxmB9TRnWsXfBvyZ2hMqq8fqUTsab_iTIPdjRg2eusutcmKnqtdA3er10=wljWHoK8Clz6ESduZgO5G2sWXRZ3G8XqGIckh45kg_xU2nObEpWiGh9CFAHTOrljysqUkjPzONWc3biqTttjb2_nTdoC1dTsBFqiSpKD9asOHk63fuE1nto30=rOn83gxEd=lwtsWvxsyeOe6BmS2Arq4Y3=nsacvZ5sFyghtsmKxfZIhUsWecb7WxEPkfG1v60U4Y01cXf05Ewho3TbibLHNOwsCZVfPK3-9jYBtZugfFRX33nmUhvCPS4Z8D1iXBXPeL_xsKPOWZMqr7re=4xx4UKefx9ojvL5kLK1llYGl6bNJUEamYiUpSOzfqbUb=vVCatVAAeMzYdNw7VnfLJZwpbCBEHi_7Ieauu047wrLxg9IATAF1Xy5N2wV_jKS5br1Wts49gyLoS1DRfqBd86X5_kmYyxoTNeknBnVYGHcmr=duJD=cvMpq43Pyyy3jnTfkWXB1hfoVJez=c4PlavsnLLLkJcmFT_uUdhCO_WEv2S9bM3-S0qAHvrn2hJzksJK8EgGYHA5O87fIiCYaAK11TUBIIjJztVP9vFPHpwFPa7eD1h77k8l470xPeezZn2nUim6klEE9xH_F2FhVcSOnMplLkJUiNLHFjBAnRgsF8EcnfJBlgr37F=TdBOFyeJSYqxpLD=DcKJDKuzv-f-cpXKXTX7Mn=zmUACkaxMSBEbbmLBdM34w27JM=CYAW=BoUKZJPLRm=VisAOeTvl7Z95ion9otJ-4q-gRPdEyl3TThSjp0vgdR4tFIFv=OTirnTdxFkcylelyq6AE4-pxYxB1oy5M4fRFUfx-gANysism6xVFjm7Po5BdeaRStyP9350sPayF1XaIN-ueCrOjo_lmyhUdqd7hCOrX7x9wWSxiuWAnhjjkP0Da9hDh=_RmMW8YILdhr21MtnCIBjDK4pfwMYBub7SAZo1p=fzNcRfGPnSJe_iTHlh2iVMlN4ryLR5CflIz37D6nnq-CL2YcUGrDqOE8opBZZjc7_xgaeJdnG1M4A19PxKw8eYl7Ai9PR3pFo-pW5tGxMNhgSMysrqX5ZIRhjWOITYI9yLhK_ESdVOj9blmU0RTVn-9K4X1EWR5nScUP9ro3_ulMhSY0elHXD0aeGpBg6awfECx90NeD4l_cX4yE_GmllHrJN=NA9-gypr08SZc9=DRVNcv_bOXGYgnadG_HKBTtmDpeT3AWx8rgnFshbmoyV6xa8zA=DeRKu6PO5Syqbg29I2CEE9okG=-yMsfa0baK2WqLjxG_ls0Tu7267WzUjk6nC-n9_cvhxz41hY-dX0XbhuIwpzem2mT7vWxngbSawuWRXprr=A779GJzUSFHbWHUeJGCq7R9xHO7ApDt_Xn254y93fsxDcoo8xtc1McFmqbHYlIKdLegSrw5iF1Swcw0oJz8vZ7RzZn2acV4ioMfLPG=PSBmr6KTkiinhVWMS7kJAuAo=g5NrhOZO-8pXtm=-ysVrYKKYLabmHj03yql=eeodKOd-ol3RMA=qv73aLdg4OyOzXfx3ZpLgvGwllc1eydEjSbFUtvKLMMRRX4koxKoG2Z=l7LG2LKGuVTRXmDsBL9ilPqZBefCoGOw2k=XCYuwaZRxAf0K_msJj-EW9Vjyn9vBz4ilkNBWRMIwwgD6rgD13ifIs=j5DZ2NNrD0hbEEdXMifY9LCJS4zhCH9ced-zv-g_hHjBZL',
        'htc6j8njvn-b': '6teys7',
        'htc6j8njvn-c': 'AIA8aISCAQAAcI7CzUr5oimasPtPjcgVXz-Sct0TAuArvQh8RNuuLfZAiyI9', #seed=(\s*)&
        'htc6j8njvn-d': 'ABaChIjBTKGNgUGAQZIQhISi0eIApJmhDgDbri32QIsiPQAAAABuAWLeAAmVfDiR7OpoMtvN1rwA8pE',
        'htc6j8njvn-f': 'A5JgcYSCAQAAN1Eyh1m1OEcpWE3AxsI5A_xXyMttxQWqMNctEkI4wATINOHDAbknjb-uci7ywH8AAEB3AAAAAA==',
        'htc6j8njvn-z': 'q',
    }
    # url = 'https://www.tiktok.com/api/v3/register/verification/age/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=1&browser_language=en&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F103.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7129986638319289862&device_platform=web_pc&focus_state=true&from_page=&history_len=2&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=&referer=&region=FR&screen_height=1080&screen_width=1920&tz_name=Europe%2FParis&webcast_language=en&msToken=gzykK1ETstTCeYKjIVe4dqDNwxhniloG_x0Fr5w1TpeJFZ1fjYFG_8_FKGTRLMatXBwyWzRCUY5oJ0HvPxOtVa-jjrH9mw16WOdclrv3JxZLXmqxPhIsZbD45WLN0Q==&X-Bogus=DFSzswVL8OEZHXJAS6RssTXyYJUU&_signature=_02B4Z6wo00001FL3dvwAAIDBcVZYULlKOERS93JAAHZWf9'
    # print(json.dumps(dict(parse_qsl(urlsplit(url).query)), indent=4))
